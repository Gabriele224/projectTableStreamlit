import streamlit as st
from fpdf import *
from io import *
PATH_TABELLINA=r"C:\Users\g.ricca\Documents\projecttabellinastreamlit\PDFTABELLINA\table.pdf"

st.title("Generatore PDF delle Tabelline")

numero1= st.number_input("Inserisci il numero\n",max_value=100)


def stampa_quadrato_tabelline(numero1):
    """Stampa nel terminale e restituisce la tabella come matrice"""
    print("\nQuadrato magico delle tabelline fino a", numero1)
    # Intestazione
    print("    " + "".join(f"{i:4}" for i in range(1, numero1 + 1)))
    print("-" * (5 * numero1))
    tabella = []
    for i in range(1, numero1 + 1):
        riga = [i * j for j in range(1, numero1 + 1)]
        print(f"{i:2} |" + "".join(f"{val:4}" for val in riga))
        tabella.append(riga)
    return tabella

def salva_quadrato_in_pdf(tabella, max_colonne_per_pagina=10, max_righe_per_pagina=10):
    """Genera PDF con più pagine se ci sono troppe colonne"""
    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.set_font("Arial", size=12)
    cella_larghezza = 10
    cella_altezza = 6

    # Calcoliamo quante pagine occorrono e dividiamo la tabella in blocchi di colonne
    num_colonne = numero1
    # Calcoliamo quante pagine occorrono e dividiamo la tabella in blocchi di colonne e righe
    num_colonne = numero1
    num_righe = numero1

    for start_riga in range(1, num_righe + 1, max_righe_per_pagina):
        end_riga = min(start_riga + max_righe_per_pagina - 1, num_righe)
        
        for start_col in range(1, num_colonne + 1, max_colonne_per_pagina):
            end_col = min(start_col + max_colonne_per_pagina - 1, num_colonne)
            
            pdf.add_page()
            pdf.cell(0, 8, txt=f"Quadrato magico delle tabelline ({start_riga}-{end_riga}) righe, ({start_col}-{end_col}) colonne", ln=True, align="C")
            pdf.ln(4)

            # Intestazione colonne
            pdf.cell(cella_larghezza, cella_altezza, "", border=1)
            for j in range(start_col, end_col + 1):
                pdf.cell(cella_larghezza, cella_altezza, str(j), border=1, align="C")
            pdf.ln(cella_altezza)

            # Corpo della tabella
            for i in range(start_riga, end_riga + 1):
                pdf.cell(cella_larghezza, cella_altezza, str(i), border=1, align="C")
                for j in range(start_col, end_col + 1):
                    pdf.cell(cella_larghezza, cella_altezza, str(tabella[i - 1][j - 1]), border=1, align="C")
                pdf.ln(cella_altezza)

                # Se la pagina è troppo piena verticalmente, aggiungiamo una nuova pagina
                if pdf.get_y() > 190:
                    pdf.add_page("L")
                    pdf.ln(10)
                    pdf.cell(0, 8, txt=f"(continua) Righe {start_riga}-{end_riga} Colonne {start_col}-{end_col}", ln=True, align="C")
        break
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer


if numero1 > 0:
    tabella = stampa_quadrato_tabelline(numero1)
    pdf_buffer = salva_quadrato_in_pdf(tabella, max_colonne_per_pagina=10, max_righe_per_pagina=10)

    st.success(f"✅ Tabellina del {numero1} generata con successo!")

    # Bottone per scaricare il PDF
    st.download_button(
        label="📥 Scarica PDF Tabellina",
        data=pdf_buffer,
        file_name=f"tabellina_{numero1}.pdf",
        mime="application/pdf"
    )
