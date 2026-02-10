#get claim details by calling claim ID

import pandas as pd
import sys

# Load data
claims_df = pd.read_csv('claims.csv')
members_df = pd.read_csv('members.csv')

def get_claim_by_id(claim_id):
    """Get claim details by ID"""
    claim = claims_df[claims_df['claim_id'] == claim_id]
    
    if claim.empty:
        print(f"No claim found with ID: {claim_id}")
        return
    
    # Get member info
    member_id = claim.iloc[0]['member_id']
    member = members_df[members_df['member_id'] == member_id]
    
    print("\n" + "="*60)
    print("CLAIM DETAILS:")
    print("="*60)
    print(claim.to_string(index=False))
    
    if not member.empty:
        print("\n" + "="*60)
        print("MEMBER INFO:")
        print("="*60)
        print(member.to_string(index=False))
    
    print("\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python query.py CLM-00001")
        print("\nOr try a random claim ID like: CLM-00042, CLM-00123, CLM-01234")
        sys.exit(1)
    
    claim_id = sys.argv[1]
    get_claim_by_id(claim_id)