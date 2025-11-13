#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
Twitter/X Integration Tools
Basic operations for posting, searching, and engaging with Twitter/X content
"""

import os
import sys
import json
import argparse
import tweepy


def get_twitter_client():
    """Initialize and return authenticated Twitter API client"""
    api_key = os.getenv('X_API_KEY')
    api_secret = os.getenv('X_API_SECRET')
    access_token = os.getenv('X_ACCESS_TOKEN')
    access_token_secret = os.getenv('X_ACCESS_TOKEN_SECRET')

    if not all([api_key, api_secret, access_token, access_token_secret]):
        print("Error: Missing Twitter API credentials", file=sys.stderr)
        print("Required environment variables:", file=sys.stderr)
        print("  X_API_KEY", file=sys.stderr)
        print("  X_API_SECRET", file=sys.stderr)
        print("  X_ACCESS_TOKEN", file=sys.stderr)
        print("  X_ACCESS_TOKEN_SECRET", file=sys.stderr)
        sys.exit(1)

    try:
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        return client
    except Exception as e:
        print(f"Error authenticating with Twitter API: {e}", file=sys.stderr)
        sys.exit(1)


# Tweet Operations

def post_tweet(text):
    """Post a new tweet"""
    client = get_twitter_client()

    if len(text) > 280:
        print(f"Error: Tweet exceeds 280 characters ({len(text)} chars)", file=sys.stderr)
        sys.exit(1)

    try:
        response = client.create_tweet(text=text)
        tweet_id = response.data['id']
        print(json.dumps({
            "success": True,
            "tweet_id": tweet_id,
            "text": text,
            "url": f"https://twitter.com/i/status/{tweet_id}"
        }, indent=2))
    except Exception as e:
        print(f"Error posting tweet: {e}", file=sys.stderr)
        sys.exit(1)


def reply_to_tweet(tweet_id, text):
    """Reply to an existing tweet"""
    client = get_twitter_client()

    if len(text) > 280:
        print(f"Error: Reply exceeds 280 characters ({len(text)} chars)", file=sys.stderr)
        sys.exit(1)

    try:
        response = client.create_tweet(text=text, in_reply_to_tweet_id=tweet_id)
        reply_id = response.data['id']
        print(json.dumps({
            "success": True,
            "reply_id": reply_id,
            "in_reply_to": tweet_id,
            "text": text,
            "url": f"https://twitter.com/i/status/{reply_id}"
        }, indent=2))
    except Exception as e:
        print(f"Error replying to tweet: {e}", file=sys.stderr)
        sys.exit(1)


def delete_tweet(tweet_id):
    """Delete a tweet"""
    client = get_twitter_client()

    try:
        client.delete_tweet(tweet_id)
        print(json.dumps({
            "success": True,
            "deleted_tweet_id": tweet_id,
            "message": "Tweet deleted successfully"
        }, indent=2))
    except Exception as e:
        print(f"Error deleting tweet: {e}", file=sys.stderr)
        sys.exit(1)


# Search & Discovery

def search_tweets(query, max_results=10):
    """Search for tweets matching a query"""
    client = get_twitter_client()

    try:
        tweets = client.search_recent_tweets(
            query=query,
            max_results=min(max_results, 100),
            tweet_fields=['created_at', 'author_id', 'public_metrics']
        )

        if not tweets.data:
            print(json.dumps({
                "success": True,
                "count": 0,
                "tweets": [],
                "message": "No tweets found"
            }, indent=2))
            return

        results = []
        for tweet in tweets.data:
            results.append({
                "id": tweet.id,
                "text": tweet.text,
                "created_at": tweet.created_at.isoformat() if tweet.created_at else None,
                "author_id": tweet.author_id,
                "metrics": {
                    "likes": tweet.public_metrics['like_count'],
                    "retweets": tweet.public_metrics['retweet_count'],
                    "replies": tweet.public_metrics['reply_count']
                },
                "url": f"https://twitter.com/i/status/{tweet.id}"
            })

        print(json.dumps({
            "success": True,
            "count": len(results),
            "query": query,
            "tweets": results
        }, indent=2))
    except Exception as e:
        print(f"Error searching tweets: {e}", file=sys.stderr)
        sys.exit(1)


def get_timeline(max_results=10):
    """Get tweets from home timeline"""
    client = get_twitter_client()

    try:
        # Get authenticated user's ID first
        me = client.get_me()
        user_id = me.data.id

        tweets = client.get_users_mentions(
            id=user_id,
            max_results=min(max_results, 100),
            tweet_fields=['created_at', 'author_id', 'public_metrics']
        )

        if not tweets.data:
            print(json.dumps({
                "success": True,
                "count": 0,
                "tweets": [],
                "message": "No tweets in timeline"
            }, indent=2))
            return

        results = []
        for tweet in tweets.data:
            results.append({
                "id": tweet.id,
                "text": tweet.text,
                "created_at": tweet.created_at.isoformat() if tweet.created_at else None,
                "author_id": tweet.author_id,
                "url": f"https://twitter.com/i/status/{tweet.id}"
            })

        print(json.dumps({
            "success": True,
            "count": len(results),
            "tweets": results
        }, indent=2))
    except Exception as e:
        print(f"Error getting timeline: {e}", file=sys.stderr)
        sys.exit(1)


# Engagement

def like_tweet(tweet_id):
    """Like a tweet"""
    client = get_twitter_client()

    try:
        # Get authenticated user's ID
        me = client.get_me()
        user_id = me.data.id

        client.like(user_id=user_id, tweet_id=tweet_id)
        print(json.dumps({
            "success": True,
            "tweet_id": tweet_id,
            "action": "liked"
        }, indent=2))
    except Exception as e:
        print(f"Error liking tweet: {e}", file=sys.stderr)
        sys.exit(1)


def unlike_tweet(tweet_id):
    """Unlike a tweet"""
    client = get_twitter_client()

    try:
        # Get authenticated user's ID
        me = client.get_me()
        user_id = me.data.id

        client.unlike(user_id=user_id, tweet_id=tweet_id)
        print(json.dumps({
            "success": True,
            "tweet_id": tweet_id,
            "action": "unliked"
        }, indent=2))
    except Exception as e:
        print(f"Error unliking tweet: {e}", file=sys.stderr)
        sys.exit(1)


def retweet(tweet_id):
    """Retweet a tweet"""
    client = get_twitter_client()

    try:
        # Get authenticated user's ID
        me = client.get_me()
        user_id = me.data.id

        client.retweet(user_id=user_id, tweet_id=tweet_id)
        print(json.dumps({
            "success": True,
            "tweet_id": tweet_id,
            "action": "retweeted"
        }, indent=2))
    except Exception as e:
        print(f"Error retweeting: {e}", file=sys.stderr)
        sys.exit(1)


def undo_retweet(tweet_id):
    """Remove a retweet"""
    client = get_twitter_client()

    try:
        # Get authenticated user's ID
        me = client.get_me()
        user_id = me.data.id

        client.unretweet(user_id=user_id, source_tweet_id=tweet_id)
        print(json.dumps({
            "success": True,
            "tweet_id": tweet_id,
            "action": "unretweeted"
        }, indent=2))
    except Exception as e:
        print(f"Error removing retweet: {e}", file=sys.stderr)
        sys.exit(1)


# User Management

def get_user_info(username):
    """Get detailed information about a user"""
    client = get_twitter_client()

    try:
        user = client.get_user(
            username=username,
            user_fields=['created_at', 'description', 'public_metrics', 'verified']
        )

        if not user.data:
            print(f"Error: User @{username} not found", file=sys.stderr)
            sys.exit(1)

        u = user.data
        print(json.dumps({
            "success": True,
            "user": {
                "id": u.id,
                "username": u.username,
                "name": u.name,
                "description": u.description,
                "created_at": u.created_at.isoformat() if u.created_at else None,
                "verified": getattr(u, 'verified', False),
                "metrics": {
                    "followers": u.public_metrics['followers_count'],
                    "following": u.public_metrics['following_count'],
                    "tweets": u.public_metrics['tweet_count']
                },
                "url": f"https://twitter.com/{u.username}"
            }
        }, indent=2))
    except Exception as e:
        print(f"Error getting user info: {e}", file=sys.stderr)
        sys.exit(1)


def follow_user(username):
    """Follow a user"""
    client = get_twitter_client()

    try:
        # Get authenticated user's ID
        me = client.get_me()
        my_user_id = me.data.id

        # Get target user's ID
        user = client.get_user(username=username)
        target_user_id = user.data.id

        client.follow_user(user_id=my_user_id, target_user_id=target_user_id)
        print(json.dumps({
            "success": True,
            "action": "followed",
            "username": username,
            "user_id": target_user_id
        }, indent=2))
    except Exception as e:
        print(f"Error following user: {e}", file=sys.stderr)
        sys.exit(1)


def unfollow_user(username):
    """Unfollow a user"""
    client = get_twitter_client()

    try:
        # Get authenticated user's ID
        me = client.get_me()
        my_user_id = me.data.id

        # Get target user's ID
        user = client.get_user(username=username)
        target_user_id = user.data.id

        client.unfollow_user(source_user_id=my_user_id, target_user_id=target_user_id)
        print(json.dumps({
            "success": True,
            "action": "unfollowed",
            "username": username,
            "user_id": target_user_id
        }, indent=2))
    except Exception as e:
        print(f"Error unfollowing user: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Twitter/X Integration Tools')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Tweet operations
    post_parser = subparsers.add_parser('post-tweet', help='Post a new tweet')
    post_parser.add_argument('text', help='Tweet content')

    reply_parser = subparsers.add_parser('reply-to-tweet', help='Reply to a tweet')
    reply_parser.add_argument('tweet_id', help='Tweet ID to reply to')
    reply_parser.add_argument('text', help='Reply content')

    delete_parser = subparsers.add_parser('delete-tweet', help='Delete a tweet')
    delete_parser.add_argument('tweet_id', help='Tweet ID to delete')

    # Search & discovery
    search_parser = subparsers.add_parser('search-tweets', help='Search tweets')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--max-results', type=int, default=10, help='Max results')

    timeline_parser = subparsers.add_parser('get-timeline', help='Get home timeline')
    timeline_parser.add_argument('--max-results', type=int, default=10, help='Max results')

    # Engagement
    like_parser = subparsers.add_parser('like-tweet', help='Like a tweet')
    like_parser.add_argument('tweet_id', help='Tweet ID to like')

    unlike_parser = subparsers.add_parser('unlike-tweet', help='Unlike a tweet')
    unlike_parser.add_argument('tweet_id', help='Tweet ID to unlike')

    retweet_parser = subparsers.add_parser('retweet', help='Retweet a tweet')
    retweet_parser.add_argument('tweet_id', help='Tweet ID to retweet')

    unretweet_parser = subparsers.add_parser('undo-retweet', help='Remove a retweet')
    unretweet_parser.add_argument('tweet_id', help='Tweet ID to unretweet')

    # User management
    user_info_parser = subparsers.add_parser('get-user-info', help='Get user information')
    user_info_parser.add_argument('username', help='Twitter username (without @)')

    follow_parser = subparsers.add_parser('follow-user', help='Follow a user')
    follow_parser.add_argument('username', help='Twitter username to follow')

    unfollow_parser = subparsers.add_parser('unfollow-user', help='Unfollow a user')
    unfollow_parser.add_argument('username', help='Twitter username to unfollow')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Execute commands
    if args.command == 'post-tweet':
        post_tweet(args.text)
    elif args.command == 'reply-to-tweet':
        reply_to_tweet(args.tweet_id, args.text)
    elif args.command == 'delete-tweet':
        delete_tweet(args.tweet_id)
    elif args.command == 'search-tweets':
        search_tweets(args.query, args.max_results)
    elif args.command == 'get-timeline':
        get_timeline(args.max_results)
    elif args.command == 'like-tweet':
        like_tweet(args.tweet_id)
    elif args.command == 'unlike-tweet':
        unlike_tweet(args.tweet_id)
    elif args.command == 'retweet':
        retweet(args.tweet_id)
    elif args.command == 'undo-retweet':
        undo_retweet(args.tweet_id)
    elif args.command == 'get-user-info':
        get_user_info(args.username)
    elif args.command == 'follow-user':
        follow_user(args.username)
    elif args.command == 'unfollow-user':
        unfollow_user(args.username)


if __name__ == '__main__':
    main()
