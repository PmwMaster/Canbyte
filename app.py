import os
from flask import Flask
from flask_login import LoginManager
from models.models import db, Usuario
from routes.pessoas import pessoas_bp
from routes.reconhecimento import reconhecimento_bp
from routes.dashboard import dashboard_bp
from routes.auth import auth_bp

def create_app():
    app = Flask(__name__)
    
    # Configurações do banco de dados e chave secreta para as flash messages
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database', 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'uma_chave_super_secreta_aqui'

    # Limite máximo de upload (ex: 16MB)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    
    db.init_app(app)
    
    # Configurar Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Por favor, faça login para acessar esta página."
    login_manager.login_message_category = "info"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Registrar rotas
    app.register_blueprint(pessoas_bp)
    app.register_blueprint(reconhecimento_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(auth_bp)

    with app.app_context():
        # Cria as tabelas caso não existam
        db.create_all()
        
        # Criar usuário admin inicial se não existir
        if not Usuario.query.filter_by(username='admin').first():
            admin = Usuario(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Usuário 'admin' criado com sucesso (senha: admin123)")

    return app

if __name__ == '__main__':
    app = create_app()
    # host='0.0.0.0' permite que outros dispositivos na mesma rede (como seu iPhone) acessem o sistema
    app.run(debug=True, host='0.0.0.0', port=5000)
