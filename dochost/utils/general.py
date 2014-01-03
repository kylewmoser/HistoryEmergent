from dochost import db


def insert_in_filename(orig, insertion):
    dotpos = orig.rfind('.')
    return orig[:dotpos] + insertion + orig[dotpos:]


def get_all(model):
    """Get all instances of model."""
    return model.query.all()


def get_model(model, uid):
    """Get the model instance of uid."""
    return model.query.get(uid)


def delete_model(model_obj):
    """Delete model."""
    db.session.delete(model_obj)
    db.session.commit()


def add_model(model_obj):
    """Add model."""
    db.session.add(model_obj)
    db.session.commit()