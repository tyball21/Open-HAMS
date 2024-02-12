from flask_smorest import Blueprint                                                      
                                                                                              
def create_api_blueprint():                                                              
    api_blueprint = Blueprint('api', __name__, url_prefix='/api', description='API for OpenHAMS')                                                                                 
                                                                                              
    # Register API endpoints                                                             
    from .zoo_api import blp as zoo_blp                                                  
    api_blueprint.register_blueprint(zoo_blp)                                            
                                                                                        
    # Repeat for other API blueprints                                                    
    # ...                                                                                
                                                                                        
    return api_blueprint