import sqlite3
import sys

def clean_db():
    conn = sqlite3.connect('backend/cdd_pro.db')
    c = conn.cursor()
    
    # 1. Get all degree_ids that have code IS NULL
    c.execute("SELECT id FROM degrees WHERE code IS NULL")
    old_degrees = [row[0] for row in c.fetchall()]
    
    if not old_degrees:
        print("No old degrees to delete.")
        return
        
    old_deg_str = ",".join("?" for _ in old_degrees)
    
    # 2. Get all module_ids
    c.execute(f"SELECT id FROM modules WHERE degree_id IN ({old_deg_str})", old_degrees)
    old_modules = [row[0] for row in c.fetchall()]
    
    if old_modules:
        old_mod_str = ",".join("?" for _ in old_modules)
        # 3. Get all LO ids
        c.execute(f"SELECT id FROM learning_outcomes WHERE module_id IN ({old_mod_str})", old_modules)
        old_los = [row[0] for row in c.fetchall()]
        
        if old_los:
            old_lo_str = ",".join("?" for _ in old_los)
            # 4. Delete CEs
            c.execute(f"DELETE FROM evaluation_criteria WHERE learning_outcome_id IN ({old_lo_str})", old_los)
            print(f"Deleted {c.rowcount} CEs")
            
            # 5. Delete LOs
            c.execute(f"DELETE FROM learning_outcomes WHERE module_id IN ({old_mod_str})", old_modules)
            print(f"Deleted {c.rowcount} LOs")
            
        # 6. Delete Modules
        c.execute(f"DELETE FROM modules WHERE degree_id IN ({old_deg_str})", old_degrees)
        print(f"Deleted {c.rowcount} Modules")
        
    # 7. Delete Degrees
    c.execute(f"DELETE FROM degrees WHERE code IS NULL")
    print(f"Deleted {c.rowcount} Degrees")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    clean_db()
