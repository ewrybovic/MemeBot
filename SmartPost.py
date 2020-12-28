from collections import deque
import csv

class SmartPost:
    def __init__(self):
        self.previous_posts_file = 'previous_posts.csv'
        self.previous_posts_deque = deque(maxlen = 15)
        self.filters = ['v.redd.it', 'youtube.com']

        # Read from the file
        with open(self.previous_posts_file, 'r+', newline='') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                for previous_posts in row:
                    self.previous_posts_deque.append(previous_posts)
        
        print(self.previous_posts_deque)
    
    '''
    Adds a post url to the deque and then writes it to the file
    '''
    def AddPost(self, post):
        self.previous_posts_deque.append(post)

        with open(self.previous_posts_file, 'w+', newline='') as previous_file:
            csv_file = csv.writer(previous_file, delimiter=',')
            csv_file.writerow(self.previous_posts_deque)

    '''
    Returns the deque that holds the previous urls
    '''
    def GetPreviousPosts(self):
        return self.previous_posts_deque

    '''
    Checks if the new post url is in the previous post deque and checks if filters are in the url
        if the url is in the post then return false
        if not then add the post and return true
    '''
    def CheckValidPost(self, post):
        if post not in self.previous_posts_deque:

            # Check if the filters are in the post, if so then return false
            for filter in self.filters:
                if filter in post:
                    return False

            self.AddPost(post)
            return True
        else:
            return False



if __name__ == '__main__':
    smart_post = SmartPost()
    if smart_post.CheckValidPost("youtube.com"):
        print("Post Added")
    else:
        print("That would be repost")
    