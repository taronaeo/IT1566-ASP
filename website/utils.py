def check_filename(filename):
  return '.' in filename and filename.split('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}
