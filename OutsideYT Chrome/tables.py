class UploadTableUnit:
    index = 0

    def __init__(self, user="-def", video="-def", preview="-def",
                 title="-def", description="-def", playlist="-def",
                 tags="-def", ends="random", cards=1, publ_time=None,
                 access=0, save_title=False):
        self.index = UploadTableUnit.index + 1
        self.user = user
        self.video = video
        self.preview = preview
        self.title = title
        self.description = description
        self.playlist = playlist
        self.tags = tags
        self.ends = ends
        self.cards = cards
        self.publ_time = publ_time
        self.access = access
        self.save_title = save_title

    def user(self):
        pass


class WatchTableUnit:
    pass

class DownloadTableUnit:
    pass