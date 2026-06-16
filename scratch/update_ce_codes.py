import sqlite3

conn = sqlite3.connect('backend/cdd_pro.db')
c = conn.cursor()

c.execute("SELECT id, learning_outcome_id, ce_code FROM evaluation_criteria")
ces = c.fetchall()

updated = 0
for ce in ces:
    ce_id = ce[0]
    lo_id = ce[1]
    ce_code = ce[2]
    
    # Get ra_number
    c.execute("SELECT ra_number FROM learning_outcomes WHERE id = ?", (lo_id,))
    ra_row = c.fetchone()
    if not ra_row:
        continue
    ra_num = ra_row[0]
    
    # Clean ce_code
    clean_code = ce_code.replace(')', '').strip()
    if clean_code.startswith('CE'):
        continue # Already formatted
        
    new_code = f"CE{ra_num}{clean_code}."
    
    c.execute("UPDATE evaluation_criteria SET ce_code = ? WHERE id = ?", (new_code, ce_id))
    updated += 1

conn.commit()
print(f"Updated {updated} CE codes in DB.")
conn.close()
