import sqlite3

def fix_db():
    conn = sqlite3.connect('backend/cdd_pro.db')
    c = conn.cursor()
    c.execute("UPDATE degrees SET level = 'BASICA' WHERE level = 'Grado Básico'")
    c.execute("UPDATE degrees SET level = 'MEDIO' WHERE level = 'Grado Medio'")
    c.execute("UPDATE degrees SET level = 'SUPERIOR' WHERE level = 'Grado Superior'")
    c.execute("UPDATE degrees SET level = 'ESPECIALIZACION' WHERE level = 'Curso de Especialización'")
    conn.commit()
    conn.close()
    print("Base de datos corregida correctamente.")

if __name__ == '__main__':
    fix_db()
