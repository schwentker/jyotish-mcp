#!/usr/bin/env python3
"""
Varga Calculator - Divisional charts (D1-D60)
"""

import sys
import json
import os

# Chart cache
CHARTS_DIR = os.path.join(os.path.dirname(__file__), '.charts_cache')


def read_divisional_chart(chart_id, varga):
    """
    Read divisional chart (currently returns D1 only, D9+ to be implemented)
    
    Args:
        chart_id: Birth chart UUID
        varga: Divisional chart type (D1, D9, D10, etc.)
    
    Returns:
        dict with divisional chart positions
    """
    try:
        # Load birth chart
        cache_file = os.path.join(CHARTS_DIR, f'{chart_id}.json')
        if not os.path.exists(cache_file):
            return {'error': f'Chart {chart_id} not found'}
        
        with open(cache_file, 'r') as f:
            chart = json.load(f)
        
        # For now, only D1 is available
        if varga == 'D1':
            return {
                'chart_id': chart_id,
                'varga': 'D1',
                'positions': chart['planets']
            }
        else:
            return {
                'error': f'Divisional chart {varga} not yet implemented',
                'message': f'{varga} calculation coming soon. Currently only D1 is available.'
            }
        
    except Exception as e:
        import traceback
        return {
            'error': str(e),
            'traceback': traceback.format_exc()
        }


if __name__ == '__main__':
    try:
        input_data = json.loads(sys.argv[1])
        action = input_data.get('action', 'read')
        
        if action == 'read':
            result = read_divisional_chart(
                input_data['chart_id'],
                input_data['varga']
            )
        else:
            result = {'error': f'Unknown action: {action}'}
        
        print(json.dumps(result))
        
    except Exception as e:
        import traceback
        error_result = {
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        print(json.dumps(error_result), file=sys.stderr)
        sys.exit(1)
