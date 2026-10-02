from flask import Flask, jsonify

app = Flask(__name__)

employees = [
    {
        "id": 1,
        "name": "Girish",
        "role": "DevOps Engineer"
    },
    {
        "id": 2,
        "name": "Rahul",
        "role": "Software Engineer"
    }
]


@app.route("/health")
def health():
    return jsonify({
        "status": "UP",
        "application": "employee-api"
    })


@app.route("/api/employees")
def get_employees():
    return jsonify(employees)


@app.route("/api/employees/<int:employee_id>")
def get_employee(employee_id):

    employee = next(
        (e for e in employees if e["id"] == employee_id),
        None
    )

    if employee:
        return jsonify(employee)

    return jsonify({
        "error": "Employee not found"
    }), 404


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )