from dochost import db


def insert_in_filename(orig, insertion):
    """Inserts a string in a filename right before the file extension."""
    dotpos = orig.rfind('.')
    return orig[:dotpos] + insertion + orig[dotpos:]


def get_all(model):
    """Get all instances of model."""
    return model.query.all()


def get_model(model, uid):
    """Get the model instance of uid."""
    return model.query.get(uid)


def delete_model(model_obj):
    """Delete and commit model."""
    db.session.delete(model_obj)
    db.session.commit()


def add_model(model_obj):
    """Add and commit model."""
    db.session.add(model_obj)
    db.session.commit()