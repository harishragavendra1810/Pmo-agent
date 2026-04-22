"""Test all PMO agents with sample data."""
import httpx
import json
from data.sample_data import SAMPLE_SOW, SAMPLE_MEETING_TRANSCRIPT, SAMPLE_KICKOFF_NOTES

def test_cr_agent():
    """Test Change Request Agent."""
    print('=' * 80)
    print('TEST 1: Change Request Agent')
    print('=' * 80)
    
    cr_response = httpx.post(
        'http://localhost:8000/api/v1/change-request',
        json={
            'project_id': 'PROJ-001',
            'sow': SAMPLE_SOW[:500],
            'current_content': SAMPLE_MEETING_TRANSCRIPT[:500]
        }
    ).json()
    
    print('Status:', cr_response['status'])
    print('Message:', cr_response['message'])
    if cr_response.get('data', {}).get('cr'):
        cr = cr_response['data']['cr']
        print(f"CR Title: {cr.get('title')}")
        print(f"Priority: {cr.get('priority')}")
        print(f"Timeline Impact: {cr.get('timeline_impact')}")
    else:
        print('No CR generated')
    print()


def test_plan_agent():
    """Test Project Plan Agent."""
    print('=' * 80)
    print('TEST 2: Project Plan Agent')
    print('=' * 80)
    
    plan_response = httpx.post(
        'http://localhost:8000/api/v1/project-plan',
        json={
            'project_id': 'PROJ-001',
            'project_name': 'Enterprise Dashboard',
            'sow': SAMPLE_SOW[:400],
            'meeting_notes': SAMPLE_KICKOFF_NOTES[:400]
        }
    ).json()
    
    print('Status:', plan_response['status'])
    print('Message:', plan_response['message'])
    if plan_response.get('data', {}).get('plan'):
        plan = plan_response['data']['plan']
        task_count = plan.get('task_count', len(plan.get('tasks', [])))
        print(f"Tasks: {task_count}")
        print(f"Duration: {plan.get('duration_days')} days")
        if plan.get('tasks'):
            print(f"First Task: {plan['tasks'][0].get('name')}")
    else:
        print('No plan generated')
    print()


def test_raid_agent():
    """Test RAID Log Agent."""
    print('=' * 80)
    print('TEST 3: RAID Log Agent')
    print('=' * 80)
    
    raid_response = httpx.post(
        'http://localhost:8000/api/v1/raid-log',
        json={
            'project_id': 'PROJ-001',
            'project_name': 'Enterprise Dashboard',
            'project_context': 'E-commerce dashboard with real-time analytics',
            'plan': {'tasks': []}
        }
    ).json()
    
    print('Status:', raid_response['status'])
    print('Message:', raid_response['message'])
    if raid_response.get('data', {}).get('raid_log'):
        raid = raid_response['data']['raid_log']
        item_count = raid.get('item_count', len(raid.get('items', [])))
        print(f"RAID Items: {item_count}")
        categorized = raid_response['data'].get('categorized', {})
        print(f"Risks: {categorized.get('RISK', 0)}")
        print(f"Dependencies: {categorized.get('DEPENDENCY', 0)}")
        print(f"Assumptions: {categorized.get('ASSUMPTION', 0)}")
    else:
        print('No RAID log generated')
    print()


def test_full_analysis():
    """Test Full Analysis endpoint."""
    print('=' * 80)
    print('TEST 4: Full Analysis (All Three Agents)')
    print('=' * 80)
    
    response = httpx.post(
        'http://localhost:8000/api/v1/full-analysis',
        json={
            'project_id': 'PROJ-001',
            'project_name': 'Enterprise Dashboard',
            'sow': SAMPLE_SOW[:300],
            'meeting_transcript': SAMPLE_MEETING_TRANSCRIPT[:300],
            'kickoff_notes': SAMPLE_KICKOFF_NOTES[:300]
        }
    ).json()
    
    print('Status:', response['status'])
    print('Message:', response['message'])
    
    data = response.get('data', {})
    if data.get('change_request'):
        print("✓ Change Request generated")
    if data.get('project_plan'):
        print("✓ Project Plan generated")
    if data.get('raid_log'):
        print("✓ RAID Log generated")
    print()


if __name__ == '__main__':
    try:
        test_cr_agent()
        test_plan_agent()
        test_raid_agent()
        test_full_analysis()
        
        print('=' * 80)
        print('✅ All agent tests completed successfully!')
        print('=' * 80)
        print('\nAPI Documentation available at: http://localhost:8000/docs')
        
    except Exception as e:
        print(f'Error: {str(e)}')
