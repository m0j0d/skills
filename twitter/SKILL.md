---
name: twitter
description: Twitter/X integration for posting tweets, searching content, managing engagement, and interacting with users through the X API v2
---

# Twitter/X Integration

Post tweets, search content, manage engagement, and interact with users directly from Claude Code using the X API v2.

**Based on:** [crazyrabbitLTC/mcp-twitter-server](https://github.com/crazyrabbitLTC/mcp-twitter-server) (essential tools subset)

## When to Use

- Post, reply to, or delete tweets
- Search tweets by keyword or operator
- Engage with content (like, quote, or share tweets)
- Follow or unfollow users
- Look up user profiles

## Setup

**Prerequisites:** X Developer Account at https://developer.twitter.com, Python 3.8+, and the `tweepy` library.

**Install dependency:**

```bash
pip install tweepy
```

**Authentication:** This skill uses OAuth 1.0a User Context (the preferred method for user-acting operations). OAuth 2.0 Bearer Token (App-Only) is also supported by tweepy for read-only access — pass only `bearer_token` to `tweepy.Client()` for that mode.

**Environment variables (OAuth 1.0a):**

```bash
export X_API_KEY="your_api_key"
export X_API_SECRET="your_api_secret"
export X_ACCESS_TOKEN="your_access_token"
export X_ACCESS_TOKEN_SECRET="your_access_token_secret"
```

**Getting credentials:**

1. Go to https://developer.twitter.com/en/portal/dashboard
2. Create or open an app
3. Under "Keys and tokens", generate all four OAuth 1.0a credentials
4. Enable "Read and Write" permissions in app settings
5. Set as environment variables

## Available Tools

### post_tweet

Post a new tweet to your timeline.

**Parameters:**
- `text` (string, required): Tweet content, max 280 characters

**Returns:** JSON with `tweet_id`, `text`, and `url` of the posted tweet

**Example:**
```bash
python scripts/twitter_tools.py post-tweet "Hello from Claude Code"
```

---

### reply_to_tweet

Reply to an existing tweet.

**Parameters:**
- `tweet_id` (string, required): ID of the tweet to reply to
- `text` (string, required): Reply content, max 280 characters

**Returns:** JSON with `reply_id`, `in_reply_to`, `text`, and `url`

**Example:**
```bash
python scripts/twitter_tools.py reply-to-tweet 1234567890 "Great point!"
```

---

### delete_tweet

Delete one of your tweets.

**Parameters:**
- `tweet_id` (string, required): ID of the tweet to delete

**Returns:** JSON with `deleted_tweet_id` and confirmation message

**Example:**
```bash
python scripts/twitter_tools.py delete-tweet 1234567890
```

---

### search_tweets

Search for tweets matching a query using the X API v2 recent search (7-day window on Free/Basic tiers; full archive on Pro+).

**Parameters:**
- `query` (string, required): Search query supporting X operators (`from:`, `to:`, `#hashtag`, `"exact phrase"`, `-exclude`)
- `max_results` (integer, optional): Number of results, default 10, max 100

**Returns:** JSON with `count` and array of tweet objects containing `id`, `text`, `created_at`, `author_id`, `metrics` (like_count, rt_count, reply_count), and `url`

**Example:**
```bash
python scripts/twitter_tools.py search-tweets "Claude AI" --max-results 20
python scripts/twitter_tools.py search-tweets "from:AnthropicAI" --max-results 10
```

---

### get_timeline

Get recent mentions from your timeline.

**Parameters:**
- `max_results` (integer, optional): Number of tweets, default 10, max 100

**Returns:** JSON with `count` and array of tweet objects containing `id`, `text`, `created_at`, `author_id`, and `url`

**Example:**
```bash
python scripts/twitter_tools.py get-timeline --max-results 20
```

---

### like_tweet

Like a tweet.

**Parameters:**
- `tweet_id` (string, required): ID of the tweet to like

**Returns:** JSON with `tweet_id` and `action: "liked"`

**Example:**
```bash
python scripts/twitter_tools.py like-tweet 1234567890
```

---

### unlike_tweet

Remove a like from a previously liked tweet.

**Parameters:**
- `tweet_id` (string, required): ID of the tweet to unlike

**Returns:** JSON with `tweet_id` and `action: "unliked"`

**Example:**
```bash
python scripts/twitter_tools.py unlike-tweet 1234567890
```

---

### retweet

Retweet a tweet to your followers.

**Parameters:**
- `tweet_id` (string, required): ID of the tweet to retweet

**Returns:** JSON with `tweet_id` and `action: "retweeted"`

**Example:**
```bash
python scripts/twitter_tools.py retweet 1234567890
```

---

### undo_retweet

Remove your retweet.

**Parameters:**
- `tweet_id` (string, required): ID of the tweet to unretweet

**Returns:** JSON with `tweet_id` and `action: "unretweeted"`

**Example:**
```bash
python scripts/twitter_tools.py undo-retweet 1234567890
```

---

### get_user_info

Get detailed profile information about an X user.

**Parameters:**
- `username` (string, required): X username without the @ symbol

**Returns:** JSON with user object containing `id`, `username`, `name`, `description`, `created_at`, `verified`, and `metrics` (followers, following, tweets)

**Example:**
```bash
python scripts/twitter_tools.py get-user-info AnthropicAI
```

---

### follow_user

Follow an X user.

**Parameters:**
- `username` (string, required): X username to follow, without @

**Returns:** JSON with `action: "followed"`, `username`, and `user_id`

**Example:**
```bash
python scripts/twitter_tools.py follow-user AnthropicAI
```

---

### unfollow_user

Unfollow an X user.

**Parameters:**
- `username` (string, required): X username to unfollow, without @

**Returns:** JSON with `action: "unfollowed"`, `username`, and `user_id`

**Example:**
```bash
python scripts/twitter_tools.py unfollow-user someuser
```

---

## API Tier Comparison

| Feature | Free | Basic ($200/mo) | Pro ($5,000/mo) | Enterprise (custom) |
|---------|------|-----------------|-----------------|---------------------|
| Post tweets | 1,500/month | 50,000/month | 100,000/month | Custom |
| Read tweets | Write-only | 15,000/month | 1,000,000/month | Custom |
| Search window | None | 7 days recent | Full archive | Full archive |
| User lookup | Limited | Yes | Yes | Yes |
| Engagement | Limited | Yes | Yes | Yes |

**Pay-as-you-go:** X launched a pay-per-use model (in broader rollout as of early 2026). Developers can opt into metered billing with spending caps and auto top-up instead of a fixed monthly plan. Check the [X Developer Portal](https://developer.twitter.com) for current availability.

**Recommendation:** Free tier is write-only. Use Basic ($200/mo) for read+write automation. Use Pro for high-volume or full-archive needs.

## Rate Limits

**X API v2 (varies by tier):**
- Tweet creation: 1,500/month (Free), 50,000/month (Basic)
- Read operations: write-only on Free; 15,000 tweets/month on Basic
- Like/Retweet: subject to per-app and per-user daily caps
- Search: 7-day recent window on Free/Basic; full archive on Pro+

**Best practices:**
- Implement delays between requests
- Cache results when possible
- Monitor `x-rate-limit-*` response headers
- Upgrade tier if hitting read limits

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Bad credentials | Check/regenerate API keys |
| 403 Forbidden | Insufficient permissions | Enable "Read and Write" in developer portal |
| 429 Rate Limited | Too many requests | Wait for rate limit window to reset |

## Upstream Coverage

This skill covers 12 of the upstream server's 33 core X API tools. Tools not included: `getTweetById`, `getUserTimeline`, `getRetweets`, `getFollowers`, `getFollowing`, list management (create/get/add/remove/members), `getLikedTweets`, `getHashtagAnalytics`, `getAggregatedEngagementMetrics`. The upstream also offers 20 SocialData.tools research tools (advanced search, thread analysis, network analysis, sentiment) not covered here.

## Security

- Never commit API credentials to git
- Use environment variables only
- Rotate credentials immediately if exposed
- Set minimum required permissions in the developer portal
- Monitor API usage regularly in the X Developer Portal
