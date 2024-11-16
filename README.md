<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Object Detection</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Custom CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <div class="container mt-5">
        <h1 class="text-center mb-4">Object Detection Application</h1>

        <form action="/detect" method="POST" enctype="multipart/form-data" class="mb-4">
            <div class="card p-4 shadow">
                <div class="form-group mb-3">
                    <label for="file" class="form-label">Upload an Image</label>
                    <input type="file" class="form-control" id="file" name="file">
                </div>
                <div class="form-group mb-3">
                    <label for="image_url" class="form-label">Or Enter an Image URL</label>
                    <input type="url" class="form-control" id="image_url" name="image_url" placeholder="https://example.com/image.jpg">
                </div>
                <button type="submit" class="btn btn-primary w-100">Detect Objects</button>
            </div>
        </form>

        <form action="/toggle_camera" method="POST" class="text-center">
            <input type="hidden" name="action" value="on">
            <button type="submit" class="btn btn-success">Turn Camera On</button>
        </form>
        <form action="/toggle_camera" method="POST" class="text-center mt-2">
            <input type="hidden" name="action" value="off">
            <button type="submit" class="btn btn-danger">Turn Camera Off</button>
        </form>

        <div class="text-center mt-4">
            <a href="/video_feed" class="btn btn-warning">Live Camera Feed</a>
        </div>
    </div>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
