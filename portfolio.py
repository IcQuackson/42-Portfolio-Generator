html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Student Information</title>
    <style>
        body {{font-family: Arial, sans-serif;
        }}
        h1 {{
            font-size: 28px;
            margin-bottom: 20px;
        }}
        h2 {{
            font-size: 22px;
            margin-bottom: 10px;
        }}
        table {{
            border-collapse: collapse;
            margin-bottom: 20px;
            width: 100%;
        }}
        th, td {{
            border: 1px solid #ccc;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        .project-name {{
            font-weight: bold;
        }}
        .final-mark {{
            font-weight: bold;
            margin-left: 10px;
        }}
    </style>
</head>
<body>
    <h1>Student Information</h1>
    <table>
        <tr>
            <th>Name</th>
            <td>{{name}}</td>
        </tr>
        <tr>
            <th>Photo</th>
            <td><img src="{{small_image_url}}"></td>
        </tr>
        <tr>
            <th>Email</th>
            <td>{{email}}</td>
        </tr>
        <tr>
            <th>Phone</th>
            <td>{{phone}}</td>
        </tr>
    </table>
    <h2>Completed Projects</h2>
    <table>
        <tr>
            <th>Project Name</th>
            <th>Final Mark</th>
        </tr>
        {{projects}}
    </table>
</body>
</html>
"""