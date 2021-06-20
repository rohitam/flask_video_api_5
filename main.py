from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name = {name}, views = {views}, likes = {likes})"

#db.create_all()

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video")
video_update_args.add_argument("views", type=int, help="Views of the video")
video_update_args.add_argument("likes", type=int, help="Likes on the video")


# videos = {}
# def crash_safe_no_video(video_id):
#     if video_id not in videos:
#         abort(404, message="Invalid video_id")
# def crash_safe_found_video(video_id):
#     if video_id in videos:
#         abort(409, message="video already exists")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Could not find video with id = " + str(video_id))
        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        # crash_safe_found_video(video_id)
        # args = video_put_args.parse_args()
        # videos[video_id] = args
        # return videos[video_id], 201
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video id taken already...")    
        args = video_put_args.parse_args()
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Could not find video with id = " + str(video_id) + " can not update")
        args = video_update_args.parse_args()
        
        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']
        db.session.commit()
        return result

    def delete(self, video_id):
        crash_safe_no_video(video_id)        
        del videos[video_id]
        return "aa", 204

        #return {"aa": "11111"}, 204


api.add_resource(Video, "/video/<int:video_id>")
if __name__== "__main__":
    app.run(debug=True)