from flask import Blueprint, render_template, request, jsonify, redirect, url_for

main = Blueprint("main", __name__)

@main.route("/")
def home():
    country = request.args.get("country")
    source = request.args.get("source")  
    return render_template("index.html", country=country, source=source)

@main.route("/about")
def about():
    context = {
        "name": "Isiakpona Chuks",
        "description": "With expertise in web and mobile development (ReactApp, AngularApp, Python), as well as being a Google Digital Marketing and e-commerce Specialist and Google UX Designer Specialist, I am committed to continuous learning and skill enhancement. My focus on detail and dedication to excellence align with company standards. Proficient in Microsoft Office Suite, Google Workspace, and equipped with strong communication, writing, analytical, and critical thinking skills, I am well-prepared to contribute to your team's success.",
    }
    return render_template("about.html", context=context)

@main.route('/about-us')
def about_us():
    return redirect(url_for("main.about"))

@main.route("/contact")
def contact():
    return render_template("contact.html")

@main.route("/portfolio")
def portfolio():
    projects_list = [
        {'name': 'Cinemahub', 'description': 'This is the first project.', 'endpoint': 'cinemahub'},
        {'name': 'Codebook', 'description': 'This is the second project.', 'endpoint': 'codebook'},
        {'name': 'Taskmate', 'description': 'This is the third project.', 'endpoint': 'taskmate'},
        {'name': 'Recipebook', 'description': 'This is the fourth project.', 'endpoint': 'recipebook'},
    ]
    return render_template("portfolio.html", projects=projects_list)

@main.route("/portfolio/<project>")
def project(project):
    projects_lst = ["cinemahub", "codebook", "taskmate", "recipebook"]
    if project in projects_lst:
        return render_template(f"portfolio/{project}.html")
    else:
        return redirect("/404")
    
@main.route('/portfolio/json')
def portfolio_json():
    projects = {
        "cinemahub": {
            "langauge": "python",
            "framework": "django",
            "status": "completed"
        },
        "codebook": {
            "langauge": "javascript",
            "framework": "react",
            "status": "learning"
        }
    }
    return jsonify(projects)
    
@main.route("/s")
def search():
    keyword = request.args.get("k")
    return f"{keyword}"

@main.route('/404')
def not_found_404():
    return render_template("404.html"), 404

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404