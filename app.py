from flask import Flask, request, redirect, render_template
#from reportlab.pdfgen import reportlab
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recibo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class CadastroEmpresa(db.Model):
    
    __tablename__='cadastro_empresa'
    
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    empresa = db.Column(db.String)
    razao = db.Column(db.String, nullable=False)
    cnpj = db.Column(db.String, nullable=False)
    end_empresa = db.Column(db.String)

    def __init__(self,empresa,razao,cnpj,end_empresa):
        self.empresa = empresa
        self.razao = razao
        self.cnpj = cnpj
        self.end_empresa = end_empresa

class CadastroPrestador(db.Model):
    
    __tablename__='cadastro_prestador'
    
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    nome = db.Column(db.String, nullable=False)
    cpf = db.Column(db.String, nullable=False)
    identidade = db.Column(db.String, nullable=False)
    orgao_emissor = db.Column(db.String, nullable=False)
    n_pis = db.Column(db.String,nullable=True)
    dt_nasc = db.Column(db.String, nullable=False)
    n_mae = db.Column(db.String, nullable=False)
    end_prest = db.Column(db.String, nullable=False)
    
    def __init__(self,nome,cpf,identidade,orgao_emissor,n_pis,dt_nasc,n_mae,end_prest):
        self.nome = nome
        self.cpf = cpf
        self.identidade = identidade
        self.orgao_emissor = orgao_emissor
        self.n_pis = n_pis
        self.dt_nasc = dt_nasc
        self.n_mae = n_mae
        self.end_prest = end_prest
        
class Recibos(db.Model):
    
    __tablename__='recibos'
    
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    servico = db.Column(db.String,nullable=False)
    valor_bruto = db.Column(db.Float, nullable=False)
    valor_liquido = db.Column(db.Float, nullable=False)
    pis = db.Column(db.Float, nullable=False)
    inss = db.Column(db.Float, nullable=False)
    irrf = db.Column(db.Float, nullable=False)
    iss = db.Column(db.Float, nullable=False)
    recibo = db.Column(db.LargeBinary, nullable=False)
    
    def __init__(self,servico,valor_bruto,valor_liquido,pis,inss,irrf,iss,recibo):
        self.servico = servico
        self.valor_bruto = valor_bruto
        self.valor_liquido = valor_liquido
        self.pis = pis
        self.inss = inss
        self.irrf = irrf
        self.iss = iss
        self.recibo = recibo
        

db.create_all()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/cadastro_empresa")
def cadastro_empresa():
    return render_template("cadastro_empresa.html")

@app.route("/cadastro_prestador")
def cadastro_prestador():
    return render_template('cadastro_prestador.html')

@app.route("/get_empresa",methods=['GET','POST'])
def get_empresa():
    if request.method == "POST":
        empresa = request.form.get("empresa")
        razao = request.form.get("razao")
        cnpj = request.form.get("cnpj")
        end_empresa = request.form.get("end_empresa")
        
        if empresa and razao and cnpj and end_empresa:
            g_empresa = CadastroEmpresa(empresa,razao,cnpj,end_empresa)
            db.session.add(g_empresa)
            db.session.commit()
            
    return redirect("/")

@app.route("/listar_empresas")
def listar_empresas():
    empresas = CadastroEmpresa.query.all()
    return render_template("listar_empresas.html", empresas=empresas)

@app.route("/get_prestador",methods=['GET','POST'])
def get_prestador():
    if request.method == "POST":
        nome = request.form.get("nome")
        cpf = request.form.get("cpf")
        identidade = request.form.get("identidade")
        orgao_emissor = request.form.get("orgao_emissor")
        n_pis = request.form.get("n_pis")
        dt_nasc = request.form.get("dt_nasc")
        n_mae = request.form.get("n_mae")
        end_prest = request.form.get("end_prest")
        
        if nome and cpf and identidade and orgao_emissor and n_pis and dt_nasc and n_mae and end_prest:
            g_prestador = CadastroPrestador(nome,cpf,identidade,orgao_emissor,n_pis,dt_nasc,n_mae,end_prest)
            db.session.add(g_prestador)
            db.session.commit()
            
    return redirect("/")

@app.route("/listar_prestadores")
def listar_prestadores():
    prestadores = CadastroPrestador.query.all()
    return render_template("listar_prestadores.html", prestadores=prestadores)




if __name__ == "__main__":
    app.run(debug=True)