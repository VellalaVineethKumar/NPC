#!/usr/bin/env python3
"""Comprehensive test to verify all NPC integration fixes"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_all_npc_fixes():
    """Test all aspects of NPC integration to ensure fixes work"""
    print("🧪 Testing All NPC Integration Fixes")
    print("=" * 50)
    
    try:
        # Test 1: Mock session state for Qatar + General
        import streamlit as st
        
        # Mock session state
        class MockSessionState:
            def __init__(self):
                self.selected_country = 'Qatar'
                self.selected_industry = 'General'
                self.selected_regulation = 'NPC'  # This should be set correctly now
                self.responses = {}
            
            def get(self, key, default=None):
                return getattr(self, key, default)
            
            def __contains__(self, key):
                return hasattr(self, key)
        
        # Replace st.session_state for testing
        original_session_state = st.session_state if hasattr(st, 'session_state') else None
        st.session_state = MockSessionState()
        
        # Test 2: Utils mapping
        from utils import get_regulation_and_industry_for_loader
        regulation, industry = get_regulation_and_industry_for_loader()
        
        print(f"✅ Test 1 - Utils Mapping:")
        print(f"   Input: Qatar + General")
        print(f"   Output: {regulation} + {industry}")
        print(f"   Expected: NPC + npc")
        print(f"   Result: {'PASS' if regulation == 'NPC' and industry == 'npc' else 'FAIL'}")
        print()
        
        # Test 3: Assessment questionnaire loading
        from assessment import get_questionnaire
        questionnaire = get_questionnaire('NPC', 'npc')
        
        print(f"✅ Test 2 - Questionnaire Loading:")
        print(f"   Loading: NPC/npc")
        print(f"   Sections found: {len(questionnaire.get('sections', []))}")
        print(f"   Has answer_points: {'answer_points' in questionnaire}")
        print(f"   Result: {'PASS' if len(questionnaire.get('sections', [])) == 13 and 'answer_points' in questionnaire else 'FAIL'}")
        print()
        
        # Test 4: Check section names
        sections = questionnaire.get('sections', [])
        if sections:
            print(f"✅ Test 3 - Section Names:")
            print(f"   First section: {sections[0].get('name', 'Unknown')}")
            print(f"   Last section: {sections[-1].get('name', 'Unknown')}")
            print(f"   Expected: NPC domain names (not PDPPL)")
            print(f"   Result: {'PASS' if 'PDPPL' not in sections[0].get('name', '') else 'FAIL'}")
            print()
        
        # Test 5: Answer points
        answer_points = questionnaire.get('answer_points', {})
        sample_npc_response = "Yes: The strategy is documented, covers all 12 NDP domains, and is reviewed/updated annually."
        
        print(f"✅ Test 4 - Answer Points:")
        print(f"   Total answer points: {len(answer_points)}")
        print(f"   Sample NPC response found: {sample_npc_response in answer_points}")
        print(f"   Result: {'PASS' if sample_npc_response in answer_points else 'FAIL'}")
        print()
        
        # Test 6: Compliance score calculation (dry run)
        st.session_state.responses = {
            's0_q0': sample_npc_response,
            's1_q0': 'Yes: A comprehensive architecture exists, is documented, and regularly updated.'
        }
        
        from assessment import calculate_compliance_score
        results = calculate_compliance_score('NPC', 'General')
        
        print(f"✅ Test 5 - Compliance Calculation:")
        print(f"   Called with: NPC + General")
        print(f"   Overall score: {results.get('overall_score', 0):.1f}%")
        print(f"   Section scores: {len(results.get('section_scores', {}))}")
        print(f"   Result: {'PASS' if results.get('overall_score', 0) > 0 else 'FAIL'}")
        print()
        
        # Restore original session state
        if original_session_state:
            st.session_state = original_session_state
        
        print("🎉 All tests completed!")
        print("If all tests show PASS, then the NPC integration is working correctly.")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_all_npc_fixes() 