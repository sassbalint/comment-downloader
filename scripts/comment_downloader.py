"""
Download comments from Facebook.
"""


import argparse
import facebook_scraper as fs


def main():
    """Main."""
    args = get_args()

    # get POST_ID from the URL of the post which can have the following structure:
    # https://www.facebook.com/USER/posts/POST_ID
    # https://www.facebook.com/groups/GROUP_ID/posts/POST_ID
    POST_ID = args.post_id

    # number of comments to download -- set this to True to download all comments
    MAX_COMMENTS = args.max_comments if args.max_comments > 0 else True

    # get the post (this gives a generator)
    gen = fs.get_posts(
        post_urls=[POST_ID],
        options={"comments": MAX_COMMENTS, "progress": True}
    )

    # take 1st element of the generator which is the post we requested
    post = next(gen)

    # extract the comments part
    comments = post['comments_full']

    # process comments as you want...
    def process(comment, reply=False):
        name = comment['commenter_name']
        text = comment['comment_text'].replace('\n', ' / ')
        mark = 'c' if not reply else 'r'
        print(f"{mark}\t{name}\t{text}")

    for comment in comments:
        process(comment)
        for reply in comment['replies']:
            process(reply, reply=True)


def get_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-p', '--post-id',
        help='ID of Facebook post from URL like https://www.facebook.com/USER/posts/POST_ID',
        required=True,
        type=str,
        default=argparse.SUPPRESS
    )
    parser.add_argument(
        '-n', '--max-comments',
        help='number of comments to download, omit or set to 0 for all, seems that the number of retrieved comments are always a multiple of 30',
        type=int,
        default='0'
    )
    return parser.parse_args()


if __name__ == '__main__':
    main()
