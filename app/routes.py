from flask import Blueprint, jsonify, render_template, make_response, request, abort
from app import db
from app.models.planet import Planet


planets_bp = Blueprint("planets_bp", __name__,url_prefix="/planets")


@planets_bp.route("", methods = ["GET"])
def handle_planets():
    planets_response = []
    
    if request.args.get("name"):
        planets = Planet.query.filter_by(name=request.args.get("name"))
    
    elif request.args.get("has_moons"):
        planets = Planet.query.filter(Planet.moons == request.args.get("has_moons"))
    
    elif request.args.get("order_by") == "name":
        planets = Planet.query.order_by(Planet.name)
    
    else:
        planets = Planet.query.all()
    for planet in planets:
        planets_response.append(planet.to_dict())
        
    return jsonify(planets_response), 200
    

@planets_bp.route("/<planet_id>", methods=["GET", "PATCH", "PUT", "DELETE"])
def handle_planet(planet_id):
    if not planet_id.isnumeric():
        return { "Error": f"{planet_id} must be numeric."}, 404
    planet_id = int(planet_id)
    planet = Planet.query.get(planet_id)
    if not planet:
        return { "Error": f"Planet {planet_id} was not found"}, 404
    
    elif request.method == "GET":
        return (planet.to_dict()),200
    
    elif request.method == "PATCH":
        form_data = request.get_json()
        sanitize_data(form_data)
        if 'name' in form_data:
            planet.name = request.json['name']
        if 'diameter' in form_data:
            planet.diameter = request.json['diameter']
        if 'moons' in form_data:
            planet.moons = request.json['moons']
        if 'picture' in form_data:
            planet.picture = request.json['picture']
    
        db.session.commit()

        return make_response(f"Planet #{planet.id} successfully updated")
    
    elif request.method == "PUT":
        form_data = request.get_json()
        sanitize_data(form_data)
        planet.name = form_data["name"]
        planet.diameter = form_data["diameter"]
        planet.moons = form_data["moons"]
        planet.picture = form_data["picture"]

        db.session.commit()

        return make_response(f"Planet #{planet.id} successfully updated")
    
    elif request.method == "DELETE":
        db.session.delete(planet)
        db.session.commit()
        
        return {
            "message": f"Planet with title {planet.name} has been deleted"
        }, 200
    

@planets_bp.route("", methods=["POST"])
def create_planet():
    request_data = request.get_json()
    sanitize_data(request_data)

    if "name" not in request_data or "moons" not in request_data \
        or "diameter" not in request_data or "picture" not in request_data:
        
        return jsonify({"message": "Missing data"}), 400
    
    new_planet = Planet(name=request_data["name"], diameter=request_data["diameter"], 
                moons=request_data["moons"], picture=request_data["picture"])

    db.session.add(new_planet)
    db.session.commit()

    return f"Planet {new_planet.name} created", 201

@planets_bp.route("/picturesummary", methods=["GET"])
def handle_planet_summary_params():
    if request.args.get("name"):
        planets = Planet.query.filter_by(name=request.args.get("name"))
        for planet in planets:
            if planet.moons == True:
                moon = "Yes"
            else:
                moon = "No"
            return render_template('planet_summary.html', 
                            url=planet.picture, 
                            title=planet.name,
                            diameter=planet.diameter,
                            moon=moon)

@planets_bp.route("/picturesummary/<planet_id>", methods=["GET"])
def handle_planet_summary(planet_id):
    planet = Planet.query.get(planet_id)
    if planet.moons == True:
        moon = "Yes"
    else:
        moon = "No"
    
    return render_template('planet_summary.html', 
                    url=planet.picture, 
                    title=planet.name,
                    diameter=planet.diameter,
                    moon=moon)


def sanitize_data(input_data):
    data_types = {"name":str, "diameter":str, "moons":bool, "picture":str}
    for name, val_type in data_types.items():
        try:
            assert val_type==type(input_data[name])
            print(name,type(input_data[name])) 
            
        except Exception as e:
            print(e)
            abort(400, "Bad Data")
    return input_data