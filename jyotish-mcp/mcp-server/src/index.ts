#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from "@modelcontextprotocol/sdk/types.js";
import { spawn } from "child_process";
import { existsSync } from "fs";
import { z } from "zod";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

// Get current file's directory - works regardless of where repo is cloned
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Schema definitions for tool parameters
const BirthDataSchema = z.object({
  name: z.string().optional(),
  datetime: z.string(), // ISO 8601 format
  timezone: z.string(),
  latitude: z.number().min(-90).max(90),
  longitude: z.number().min(-180).max(180),
});

const ChartIdSchema = z.object({
  chart_id: z.string().uuid(),
});

const DateSchema = z.object({
  date: z.string().optional(), // ISO 8601, defaults to now
});

const VargaSchema = z.object({
  chart_id: z.string().uuid(),
  varga: z.enum(["D1", "D2", "D3", "D7", "D9", "D10", "D12", "D30"]),
});

const CompatibilitySchema = z.object({
  chart_id_1: z.string().uuid(),
  chart_id_2: z.string().uuid(),
});

// Tool definitions
const TOOLS: Tool[] = [
  {
    name: "chart_create",
    description:
      "Calculate a complete Vedic birth chart from birth data. Returns a chart_id for future reference. Includes D1 (birth chart), D9 (navamsa), planetary positions, houses, nakshatras, and Vimshottari Dasha periods.",
    inputSchema: {
      type: "object",
      properties: {
        name: {
          type: "string",
          description: "Name of the person (optional)",
        },
        datetime: {
          type: "string",
          description: "Birth date and time in ISO 8601 format (YYYY-MM-DDTHH:MM:SS)",
        },
        timezone: {
          type: "string",
          description: "Timezone string (e.g., 'America/New_York', 'Asia/Kolkata')",
        },
        latitude: {
          type: "number",
          description: "Latitude in decimal degrees (positive for North)",
        },
        longitude: {
          type: "number",
          description: "Longitude in decimal degrees (positive for East)",
        },
      },
      required: ["datetime", "timezone", "latitude", "longitude"],
    },
  },
  {
    name: "chart_read",
    description:
      "Retrieve complete chart data for a previously calculated chart. Includes all planetary positions, houses, nakshatras, divisional charts, and dasha periods.",
    inputSchema: {
      type: "object",
      properties: {
        chart_id: {
          type: "string",
          description: "UUID of the chart to retrieve",
        },
      },
      required: ["chart_id"],
    },
  },
  {
    name: "chart_list",
    description:
      "List all stored charts with basic information (name, date, location). Useful for selecting which chart to analyze.",
    inputSchema: {
      type: "object",
      properties: {},
    },
  },
  {
    name: "dasha_current",
    description:
      "Get the current running Vimshottari Dasha periods (Maha Dasha, Antar Dasha, Pratyantar Dasha) for a chart. Can specify a date or defaults to current time. Includes ruling planets, start/end dates, and remaining balance.",
    inputSchema: {
      type: "object",
      properties: {
        chart_id: {
          type: "string",
          description: "UUID of the chart",
        },
        date: {
          type: "string",
          description: "Optional date in ISO 8601 format (defaults to now)",
        },
      },
      required: ["chart_id"],
    },
  },
  {
    name: "transit_now",
    description:
      "Get current planetary transit positions relative to the birth chart. Shows which houses planets are transiting and aspects they make to natal planets. Can specify a date or defaults to current time.",
    inputSchema: {
      type: "object",
      properties: {
        chart_id: {
          type: "string",
          description: "UUID of the chart",
        },
        date: {
          type: "string",
          description: "Optional date in ISO 8601 format (defaults to now)",
        },
      },
      required: ["chart_id"],
    },
  },
  {
    name: "divisional_read",
    description:
      "Retrieve a specific divisional chart (varga). D9 (Navamsa) is most important for relationships and dharma. Other divisions analyze specific life domains: D2 (wealth), D3 (siblings), D7 (children), D10 (career), D12 (parents), D30 (misfortunes).",
    inputSchema: {
      type: "object",
      properties: {
        chart_id: {
          type: "string",
          description: "UUID of the chart",
        },
        varga: {
          type: "string",
          enum: ["D1", "D2", "D3", "D7", "D9", "D10", "D12", "D30"],
          description: "Divisional chart type (D1=birth, D9=navamsa, etc.)",
        },
      },
      required: ["chart_id", "varga"],
    },
  },
  {
    name: "yogas_identify",
    description:
      "Identify classical yogas (planetary combinations) in a chart. Includes Raj Yogas (power/status), Dhana Yogas (wealth), Pancha Mahapurusha Yogas (great personality), and other significant combinations from classical texts.",
    inputSchema: {
      type: "object",
      properties: {
        chart_id: {
          type: "string",
          description: "UUID of the chart",
        },
      },
      required: ["chart_id"],
    },
  },
  {
    name: "compatibility_analyze",
    description:
      "Analyze compatibility between two charts for relationships. Uses traditional Kuta system, cross-aspects between charts, and comparative analysis of key factors (Moon, Venus, 7th house).",
    inputSchema: {
      type: "object",
      properties: {
        chart_id_1: {
          type: "string",
          description: "UUID of first chart",
        },
        chart_id_2: {
          type: "string",
          description: "UUID of second chart",
        },
      },
      required: ["chart_id_1", "chart_id_2"],
    },
  },
];

// Helper function to call Python calculation engine
// FIXED: No hardcoded paths - works for any clone location
async function callPythonCalculator(
  scriptName: string,
  args: Record<string, any>
): Promise<any> {
  return new Promise((resolve, reject) => {
    // Dynamic path resolution - works regardless of repo location
    // From: mcp-server/dist/index.js
    // To:   calculations/
    const calculationsPath = join(__dirname, "..", "..", "calculations");
    const scriptPath = join(calculationsPath, `${scriptName}.py`);
    
    // Check for venv Python first, fallback to system python3
    // This ensures the script works even if venv isn't set up yet
    const venvPython = join(calculationsPath, "venv", "bin", "python");
    const systemPython = "python3";
    const pythonPath = existsSync(venvPython) ? venvPython : systemPython;
    
    // Verify the Python script exists before trying to run it
    if (!existsSync(scriptPath)) {
      reject(new Error(
        `Python script not found: ${scriptPath}\n` +
        `Make sure you're running from the correct directory and ` +
        `the calculations folder exists.`
      ));
      return;
    }
    
    // Log for debugging (goes to stderr, not to Claude)
    console.error(`[Jyotish MCP] Calling: ${pythonPath} ${scriptPath}`);
    console.error(`[Jyotish MCP] CWD: ${calculationsPath}`);
    
    const python = spawn(pythonPath, [scriptPath, JSON.stringify(args)], {
      cwd: calculationsPath,
      env: { ...process.env }
    });

    let stdout = "";
    let stderr = "";

    python.stdout.on("data", (data) => {
      stdout += data.toString();
    });

    python.stderr.on("data", (data) => {
      stderr += data.toString();
    });

    python.on("close", (code) => {
      if (code !== 0) {
        reject(new Error(
          `Python script failed with code ${code}:\n${stderr}\n\n` +
          `Script: ${scriptPath}\n` +
          `Python: ${pythonPath}\n` +
          `Args: ${JSON.stringify(args)}`
        ));
      } else {
        try {
          const result = JSON.parse(stdout);
          resolve(result);
        } catch (e) {
          reject(new Error(
            `Failed to parse Python output as JSON:\n${stdout}\n\n` +
            `Parse error: ${e instanceof Error ? e.message : String(e)}`
          ));
        }
      }
    });
    
    python.on("error", (err) => {
      reject(new Error(
        `Failed to spawn Python process:\n${err.message}\n\n` +
        `Tried to run: ${pythonPath}\n` +
        `Make sure Python 3.x is installed and in your PATH.\n` +
        `You can install dependencies with: cd calculations && pip install -r requirements.txt`
      ));
    });
  });
}

// Tool handlers
async function handleChartCreate(args: any) {
  const validated = BirthDataSchema.parse(args);
  const result = await callPythonCalculator("chart_calculator", {
    action: "create",
    ...validated,
  });
  return {
    content: [
      {
        type: "text",
        text: JSON.stringify(result, null, 2),
      },
    ],
  };
}

async function handleChartRead(args: any) {
  const validated = ChartIdSchema.parse(args);
  const result = await callPythonCalculator("chart_calculator", {
    action: "read",
    ...validated,
  });
  return {
    content: [
      {
        type: "text",
        text: JSON.stringify(result, null, 2),
      },
    ],
  };
}

async function handleChartList(args: any) {
  const result = await callPythonCalculator("chart_calculator", {
    action: "list",
  });
  return {
    content: [
      {
        type: "text",
        text: JSON.stringify(result, null, 2),
      },
    ],
  };
}

async function handleDashaCurrent(args: any) {
  const validated = z
    .object({
      chart_id: z.string().uuid(),
      date: z.string().optional(),
    })
    .parse(args);
  const result = await callPythonCalculator("dasha_calculator", {
    action: "current",
    ...validated,
  });
  return {
    content: [
      {
        type: "text",
        text: JSON.stringify(result, null, 2),
      },
    ],
  };
}

async function handleTransitNow(args: any) {
  const validated = z
    .object({
      chart_id: z.string().uuid(),
      date: z.string().optional(),
    })
    .parse(args);
  const result = await callPythonCalculator("transit_calculator", {
    action: "current",
    ...validated,
  });
  return {
    content: [
      {
        type: "text",
        text: JSON.stringify(result, null, 2),
      },
    ],
  };
}

async function handleDivisionalRead(args: any) {
  const validated = VargaSchema.parse(args);
  const result = await callPythonCalculator("varga_calculator", {
    action: "read",
    ...validated,
  });
  return {
    content: [
      {
        type: "text",
        text: JSON.stringify(result, null, 2),
      },
    ],
  };
}

async function handleYogasIdentify(args: any) {
  const validated = ChartIdSchema.parse(args);
  const result = await callPythonCalculator("yoga_identifier", {
    action: "identify",
    ...validated,
  });
  return {
    content: [
      {
        type: "text",
        text: JSON.stringify(result, null, 2),
      },
    ],
  };
}

async function handleCompatibilityAnalyze(args: any) {
  const validated = CompatibilitySchema.parse(args);
  const result = await callPythonCalculator("compatibility_calculator", {
    action: "analyze",
    ...validated,
  });
  return {
    content: [
      {
        type: "text",
        text: JSON.stringify(result, null, 2),
      },
    ],
  };
}

// Main server setup
async function main() {
  const server = new Server(
    {
      name: "jyotish-mcp-server",
      version: "0.5.0",
    },
    {
      capabilities: {
        tools: {},
      },
    }
  );

  // List available tools
  server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: TOOLS,
  }));

  // Handle tool calls
  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    try {
      switch (request.params.name) {
        case "chart_create":
          return await handleChartCreate(request.params.arguments);
        case "chart_read":
          return await handleChartRead(request.params.arguments);
        case "chart_list":
          return await handleChartList(request.params.arguments);
        case "dasha_current":
          return await handleDashaCurrent(request.params.arguments);
        case "transit_now":
          return await handleTransitNow(request.params.arguments);
        case "divisional_read":
          return await handleDivisionalRead(request.params.arguments);
        case "yogas_identify":
          return await handleYogasIdentify(request.params.arguments);
        case "compatibility_analyze":
          return await handleCompatibilityAnalyze(request.params.arguments);
        default:
          throw new Error(`Unknown tool: ${request.params.name}`);
      }
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : String(error);
      return {
        content: [
          {
            type: "text",
            text: `Error: ${errorMessage}`,
          },
        ],
        isError: true,
      };
    }
  });

  // Start server
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Jyotish MCP Server v0.5.0 running on stdio");
  console.error("Repository-relative paths configured - works for any clone location");
}

main().catch((error) => {
  console.error("Fatal error in Jyotish MCP Server:", error);
  process.exit(1);
});
