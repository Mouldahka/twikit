from __future__ import annotations

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from requests import Response

    from .client import Client
    from .tweet import Tweet
    from .utils import Result


class User:
    """
    Attributes
    ----------
    id : str
        The unique identifier of the user.
    created_at : str
        The date and time when the user account was created.
    name : str
        The user's name.
    screen_name : str
        The user's screen name.
    profile_image_url : str
        The URL of the user's profile image (HTTPS version).
    profile_banner_url : str
        The URL of the user's profile banner.
    url : str
        The user's URL.
    location : str
        The user's location information.
    description : str
        The user's profile description.
    description_urls : list
        URLs found in the user's profile description.
    urls : list
        URLs associated with the user.
    pinned_tweet_ids : str
        The IDs of tweets that the user has pinned to their profile.
    is_blue_verified : bool
        Indicates if the user is verified with a blue checkmark.
    verified : bool
        Indicates if the user is verified.
    possibly_sensitive : bool
        Indicates if the user's content may be sensitive.
    can_dm : bool
        Indicates whether the user can receive direct messages.
    can_media_tag : bool
        Indicates whether the user can be tagged in media.
    want_retweets : bool
        Indicates if the user wants retweets.
    default_profile : bool
        Indicates if the user has the default profile.
    default_profile_image : bool
        Indicates if the user has the default profile image.
    has_custom_timelines : bool
        Indicates if the user has custom timelines.
    followers_count : int
        The count of followers.
    fast_followers_count : int
        The count of fast followers.
    normal_followers_count : int
        The count of normal followers.
    following_count : int
        The count of users the user is following.
    favourites_count : int
        The count of favorites or likes.
    listed_count : int
        The count of lists the user is a member of.
    media_count : int
        The count of media items associated with the user.
    statuses_count : int
        The count of tweets.
    is_translator : bool
        Indicates if the user is a translator.
    translator_type : str
        The type of translator.
    profile_interstitial_type : str
        The type of profile interstitial.
    withheld_in_countries : list[str]
        Countries where the user's content is withheld.
    """

    def __init__(self, client: Client, data: dict) -> None:
        self._client = client
        legacy = data['legacy']

        self.id: str = data['rest_id']
        self.created_at: str = legacy['created_at']
        self.name: str = legacy['name']
        self.screen_name: str = legacy['screen_name']
        self.profile_image_url: str = legacy['profile_image_url_https']
        self.profile_banner_url: str = legacy.get('profile_banner_url')
        self.url: str = legacy.get('url')
        self.location: str = legacy['location']
        self.description: str = legacy['description']
        self.description_urls: list = legacy['entities']['description']['urls']
        self.urls: list = legacy['entities'].get('url', {}).get('urls')
        self.pinned_tweet_ids: list[str] = legacy['pinned_tweet_ids_str']
        self.is_blue_verified: bool = data['is_blue_verified']
        self.verified: bool = legacy['verified']
        self.possibly_sensitive: bool = legacy['possibly_sensitive']
        self.can_dm: bool = legacy['can_dm']
        self.can_media_tag: bool = legacy['can_media_tag']
        self.want_retweets: bool = legacy['want_retweets']
        self.default_profile: bool = legacy['default_profile']
        self.default_profile_image: bool = legacy['default_profile_image']
        self.has_custom_timelines: bool = legacy['has_custom_timelines']
        self.followers_count: int = legacy['followers_count']
        self.fast_followers_count: int = legacy['fast_followers_count']
        self.normal_followers_count: int = legacy['normal_followers_count']
        self.following_count: int = legacy['friends_count']
        self.favourites_count: int = legacy['favourites_count']
        self.listed_count: int = legacy['listed_count']
        self.media_count = legacy['media_count']
        self.statuses_count: int = legacy['statuses_count']
        self.is_translator: bool = legacy['is_translator']
        self.translator_type: str = legacy['translator_type']
        self.withheld_in_countries: list[str] = legacy['withheld_in_countries']

    def get_tweets(
        self,
        tweet_type: Literal['Tweets', 'Replies', 'Media', 'Likes'],
        count: int = 40,
    ) -> Result[Tweet]:
        """
        Retrieves the user's tweets.

        Parameters
        ----------
        tweet_type : {'Tweets', 'Replies', 'Media', 'Likes'}
            The type of tweets to retrieve.
        count : int, default=40
            The number of tweets to retrieve.

        Returns
        -------
        Result[Tweet]
            A Result object containing a list of `Tweet` objects.

        Examples
        --------
        >>> user = client.get_user_by_screen_name('example_user')
        >>> tweets = user.get_tweets('Tweets', count=20)
        >>> for tweet in tweets:
        ...    print(tweet)
        <Tweet id="...">
        <Tweet id="...">
        ...
        ...

        >>> more_tweets = tweets.next  # Retrieve more tweets
        >>> for tweet in more_tweets:
        ...     print(tweet)
        <Tweet id="...">
        <Tweet id="...">
        ...
        ...
        """
        return self._client.get_user_tweets(self.id, tweet_type, count)

    def follow(self) -> Response:
        """
        Follows the user.

        Returns
        -------
        httpx.Response
            Response returned from twitter api.

        See Also
        --------
        Client.follow_user
        """
        return self._client.follow_user(self.id)

    def unfollow(self) -> Response:
        """
        Unfollows the user.

        Returns
        -------
        httpx.Response
            Response returned from twitter api.

        See Also
        --------
        Client.unfollow_user
        """
        return self._client.unfollow_user(self.id)

    def __repr__(self) -> str:
        return f'<User id="{self.id}">'

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, User) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self == __value
