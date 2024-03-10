import flask
from flask import jsonify
from . import db_session
from .jobs import Jobs

blueprint = flask.Blueprint(
    'new_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'is_finished'))
                 for item in jobs]
        }
    )
