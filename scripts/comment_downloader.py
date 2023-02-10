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

    def print_and_replies(comment):
        print(comment)
        for reply in comment['replies']:
            print('', reply, sep='\t')

    # process comments as you want...
    process = print if not args.replies else print_and_replies

    for comment in comments:
        process(comment)


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
    parser.add_argument(
        '-r', '--replies',
        help='download reply-comments as well',
        action='store_true'
    )
    return parser.parse_args()


if __name__ == '__main__':
    main()
