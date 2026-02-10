import pandas as pd
import sys

# Load data
claims_df = pd.read_csv('claims.csv')
members_df = pd.read_csv('members.csv')
policies_df = pd.read_csv('policies.csv')

def show_stats():
    print("\n" + "="*60)
    print("CLAIMS DATABASE STATISTICS")
    print("="*60 + "\n")
    
    # Overall stats
    print("OVERALL:")
    print(f"  Total Claims: {len(claims_df):,}")
    print(f"  Total Amount: ${claims_df['claim_amount'].sum():,.2f}")
    print(f"  Average Claim: ${claims_df['claim_amount'].mean():,.2f}")
    print(f"  Min Claim: ${claims_df['claim_amount'].min():,.2f}")
    print(f"  Max Claim: ${claims_df['claim_amount'].max():,.2f}")
    
    print("\nBY STATUS:")
    status_stats = claims_df.groupby('status')['claim_amount'].agg(['count', 'sum', 'mean'])
    status_stats.columns = ['Count', 'Total ($)', 'Average ($)']
    print(status_stats.to_string())
    
    print("\nBY CLAIM TYPE:")
    type_stats = claims_df.groupby('claim_type')['claim_amount'].agg(['count', 'sum', 'mean'])
    type_stats.columns = ['Count', 'Total ($)', 'Average ($)']
    print(type_stats.to_string())
    
    print("\nMEMBERS & POLICIES:")
    print(f"  Total Members: {len(members_df):,}")
    print(f"  Total Policies: {len(policies_df):,}")
    print(f"  Average Premium: ${policies_df['premium'].mean():,.2f}")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "status":
            # Stats by status
            print("\nCLAIMS BY STATUS:\n")
            print(claims_df['status'].value_counts().to_string())
            
        elif command == "type":
            # Stats by type
            print("\nCLAIMS BY TYPE:\n")
            print(claims_df['claim_type'].value_counts().to_string())
            
        elif command == "approved":
            # Approved claims
            approved = claims_df[claims_df['status'] == 'APPROVED']
            print(f"\nAPPROVED CLAIMS: {len(approved)}")
            print(f"Total Amount: ${approved['claim_amount'].sum():,.2f}")
            print(f"Average: ${approved['claim_amount'].mean():,.2f}")
            
        elif command == "denied":
            # Denied claims
            denied = claims_df[claims_df['status'] == 'DENIED']
            print(f"\nDENIED CLAIMS: {len(denied)}")
            print(f"Total Amount: ${denied['claim_amount'].sum():,.2f}")
            print(f"Average: ${denied['claim_amount'].mean():,.2f}")
            
        elif command == "pending":
            # Pending claims
            pending = claims_df[claims_df['status'] == 'PENDING']
            print(f"\nPENDING CLAIMS: {len(pending)}")
            print(f"Total Amount: ${pending['claim_amount'].sum():,.2f}")
            
        else:
            print(f"Unknown command: {command}")
            print("\nUsage: python quick_stats.py [status|type|approved|denied|pending]")
            print("Or just: python quick_stats.py (for all stats)")
    else:
        show_stats()