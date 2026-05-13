from flask import Blueprint, render_template, send_file, Response
from flask_login import login_required
from models.models import Pessoa, Imagem, HistoricoReconhecimento
from fpdf import FPDF
import io

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    return render_template('index.html')

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    total_pessoas = Pessoa.query.count()
    total_imagens = Imagem.query.count()
    total_reconhecimentos = HistoricoReconhecimento.query.count()
    
    ultimos_reconhecimentos = HistoricoReconhecimento.query.order_by(
        HistoricoReconhecimento.data_hora.desc()
    ).limit(10).all()
    
    return render_template(
        'dashboard.html', 
        total_pessoas=total_pessoas,
        total_imagens=total_imagens,
        total_reconhecimentos=total_reconhecimentos,
        ultimos_reconhecimentos=ultimos_reconhecimentos
    )

@dashboard_bp.route('/dashboard/exportar-pdf')
@login_required
def exportar_pdf():
    historia = HistoricoReconhecimento.query.order_by(HistoricoReconhecimento.data_hora.desc()).all()
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    
    # Título
    pdf.cell(190, 10, "Relatório de Reconhecimento Facial - FaceID Security", ln=True, align="C")
    pdf.ln(10)
    
    # Cabeçalho da Tabela
    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(60, 10, "Nome", 1, 0, "C", True)
    pdf.cell(50, 10, "Data/Hora", 1, 0, "C", True)
    pdf.cell(40, 10, "Confiança", 1, 0, "C", True)
    pdf.cell(40, 10, "Origem", 1, 1, "C", True)
    
    # Dados
    pdf.set_font("Arial", "", 10)
    for registro in historia:
        nome = registro.pessoa.nome if registro.pessoa else "Desconhecido"
        data = registro.data_hora.strftime("%d/%m/%Y %H:%M:%S")
        confianca = f"{registro.confianca}%"
        origem = registro.origem.capitalize()
        
        pdf.cell(60, 10, nome, 1)
        pdf.cell(50, 10, data, 1)
        pdf.cell(40, 10, confianca, 1)
        pdf.cell(40, 10, origem, 1, 1)
        
    output = io.BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    output.write(pdf_bytes)
    output.seek(0)
    
    return send_file(
        output,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='relatorio_reconhecimento.pdf'
    )
