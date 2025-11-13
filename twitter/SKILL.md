---
name: twitter
description: Twitter/X integration for posting tweets, searching content, managing engagement, and interacting with users through the Twitter API
---

# Twitter/X Integration

Post tweets, search content, manage engagement, and interact with users directly from Claude Code.

**Based on:** crazyrabbitLTC/mcp-twitter-server (essential tools subset)

## When to Use

- Post and schedule tweets
- Search tweets and monitor topics
- Engage with content (like, retweet, reply)
- Follow/unfollow users
- Read your timeline
- Manage your Twitter presence

## Setup

### Prerequisites

- Twitter Developer Account (https://developer.twitter.com)
- Twitter API credentials (Free tier works for basic operations)

### Environment Variables

```bash
export X_API_KEY="your_api_key"
export X_API_SECRET="your_api_secret"
export X_ACCESS_TOKEN="your_access_token"
export X_ACCESS_TOKEN_SECRET="your_access_token_secret"
```

### Getting Twitter API Credentials

1. Go to https://developer.twitter.com/en/portal/dashboard
2. Create a new app or use existing
3. Navigate to "Keys and tokens"
4. Generate/copy all four credentials
5. Set as environment variables

### Installation

```bash
pip install requests tweepy --break-system-packages
```

### Validation

```bash
# From project root
npm run validate:twitter

# Or directly
python integration-skills/twitter/scripts/validate.py
```

## Available Tools

### Tweet Operations

#### `post_tweet`

Post a new tweet to your timeline.

**Parameters:**
- `text` (string, required): Tweet content (max 280 characters)

**Example:**
```python
python scripts/twitter_tools.py post-tweet "Hello from Claude Code! 🤖"
```

#### `reply_to_tweet`

Reply to an existing tweet.

**Parameters:**
- `tweet_id` (string, required): ID of tweet to reply to
- `text` (string, required): Reply content (max 280 characters)

**Example:**
```python
python scripts/twitter_tools.py reply-to-tweet 1234567890 "Great point!"
```

#### `delete_tweet`

Delete one of your tweets.

**Parameters:**
- `tweet_id` (string, required): ID of tweet to delete

**Example:**
```python
python scripts/twitter_tools.py delete-tweet 1234567890
```

---

### Search & Discovery

#### `search_tweets`

Search for tweets matching a query.

**Parameters:**
- `query` (string, required): Search query (supports Twitter search operators)
- `max_results` (number, optional): Number of results to return (default: 10, max: 100)

**Example:**
```python
python scripts/twitter_tools.py search-tweets "Claude AI" --max-results 20
python scripts/twitter_tools.py search-tweets "from:ClaudeAI" --max-results 10
```

**Search operators:**
- `from:username` - Tweets from specific user
- `to:username` - Tweets mentioning user
- `#hashtag` - Tweets with hashtag
- `"exact phrase"` - Exact match
- `-word` - Exclude word

#### `get_timeline`

Get tweets from your home timeline.

**Parameters:**
- `max_results` (number, optional): Number of tweets to fetch (default: 10, max: 100)

**Example:**
```python
python scripts/twitter_tools.py get-timeline --max-results 20
```

---

### Engagement

#### `like_tweet`

Like a tweet.

**Parameters:**
- `tweet_id` (string, required): ID of tweet to like

**Example:**
```python
python scripts/twitter_tools.py like-tweet 1234567890
```

#### `unlike_tweet`

Unlike a previously liked tweet.

**Parameters:**
- `tweet_id` (string, required): ID of tweet to unlike

**Example:**
```python
python scripts/twitter_tools.py unlike-tweet 1234567890
```

#### `retweet`

Retweet a tweet to your followers.

**Parameters:**
- `tweet_id` (string, required): ID of tweet to retweet

**Example:**
```python
python scripts/twitter_tools.py retweet 1234567890
```

#### `undo_retweet`

Remove your retweet.

**Parameters:**
- `tweet_id` (string, required): ID of tweet to unretweet

**Example:**
```python
python scripts/twitter_tools.py undo-retweet 1234567890
```

---

### User Management

#### `get_user_info`

Get detailed information about a Twitter user.

**Parameters:**
- `username` (string, required): Twitter username (without @)

**Example:**
```python
python scripts/twitter_tools.py get-user-info ClaudeAI
```

**Returns:**
- User ID
- Display name
- Bio/description
- Follower count
- Following count
- Tweet count
- Account creation date
- Verified status

#### `follow_user`

Follow a Twitter user.

**Parameters:**
- `username` (string, required): Twitter username to follow (without @)

**Example:**
```python
python scripts/twitter_tools.py follow-user ClaudeAI
```

#### `unfollow_user`

Unfollow a Twitter user.

**Parameters:**
- `username` (string, required): Twitter username to unfollow (without @)

**Example:**
```python
python scripts/twitter_tools.py unfollow-user someuser
```

---

## Common Use Cases

### Monitor Brand Mentions

```python
# Search for mentions of your brand
python scripts/twitter_tools.py search-tweets "MyBrand OR @MyBrand" --max-results 50
```

### Automated Engagement

```python
# Like tweets about a topic
# (Use with caution - respect Twitter's automation rules)
python scripts/twitter_tools.py search-tweets "Claude AI helpful" --max-results 10
# Then like relevant tweets
```

### Content Monitoring

```python
# Monitor timeline for important updates
python scripts/twitter_tools.py get-timeline --max-results 20
```

### User Research

```python
# Get info about influencers in your space
python scripts/twitter_tools.py get-user-info influencer_handle
```

---

## Rate Limits

**Twitter API Free Tier Limits:**
- **Tweet creation:** 50 tweets per 24 hours
- **Read operations:** 1,500 tweets per 15 minutes (timeline, search)
- **Like/Retweet:** 1,000 per 24 hours
- **Follow:** 400 per 24 hours

**Best Practices:**
- Implement delays between requests
- Cache results when possible
- Monitor rate limit headers
- Upgrade to paid tier if needed

---

## API Tier Comparison

| Feature | Free | Basic ($100/mo) | Pro ($5,000/mo) |
|---------|------|-----------------|-----------------|
| Post tweets | ✅ 50/day | ✅ Unlimited | ✅ Unlimited |
| Search tweets | ✅ Limited | ✅ Good | ✅ Full archive |
| Timeline access | ✅ | ✅ | ✅ |
| User lookup | ✅ | ✅ | ✅ |
| Engagement | ✅ | ✅ | ✅ |

**For basic automation: Free tier is sufficient**

---

## Error Handling

Common errors and solutions:

**401 Unauthorized:**
- Check API credentials are correct
- Verify credentials have write permissions
- Regenerate tokens if needed

**429 Rate Limited:**
- Slow down request rate
- Wait for rate limit window to reset
- Consider upgrading API tier

**403 Forbidden:**
- Check app permissions in developer portal
- Ensure "Read and Write" permissions enabled
- May need to reauthorize app

---

## Security Notes

⚠️ **IMPORTANT:**
- Never commit API credentials to git
- Use environment variables only
- Rotate credentials if exposed
- Set minimum required permissions
- Monitor API usage regularly

---

## Limitations

**Not included in basic skill (requires API upgrade):**
- Advanced search (full archive)
- Follower/following lists (requires elevated access)
- Direct messages
- Media uploads (coming soon)
- Hashtag analytics
- Scheduled tweets (use external scheduler)

**Available in comprehensive version (25% reserve):**
- Full 53-tool suite with advanced research
- SocialData.tools integration
- Thread analysis
- Sentiment analysis
- Network mapping

---

## Navigation

- [← Back to Integration Skills](../README.md)
- [Twitter Developer Portal](https://developer.twitter.com)
- [Twitter API Documentation](https://developer.twitter.com/en/docs/twitter-api)
