# (file: createmydb.sh)

# Script to create my database declaratively

set echo true

# Use this to ignore errors and continue, if needed
# set ignoreErrors true

# Create database
create database plocal:../databases/mixedemotions root root plocal graph

# Create User vertex
create class User extends V

# Create User property
create property User.lang                                   STRING
create property User.profile_background_image_url_https     STRING
# Debajo podria ser BOOLEAN
create property User.verified                               STRING
create property User.withheld_scope                         STRING
create property User.location                               STRING
# Debajo podria ser BOOLEAN
create property User.follow_request_sent                    STRING
create property User.profile_background_color               STRING
# Debajo podria ser BOOLEAN
create property User.contributors_enabled                   STRING
create property User.profile_sidebar_fill_color             STRING
create property User.profile_link_color                     STRING
create property User.id                                     LONG
create property User.profile_image_url_https                STRING
create property User.id_str                                 STRING
create property User.withheld_in_countries                  STRING
create property User.profile_sidebar_border_color           STRING
create property User.utc_offset                             STRING
# Debajo podría ser BOOLEAN
create property User.is_translator                          STRING
# Debajo podría ser BOOLEAN
create property User.profile_use_background_image           STRING
# Debajo podría ser BOOLEAN
create property User.protected                              STRING
# Debajo podría ser BOOLEAN
create property User.show_all_inline_media                  STRING
create property User.profile_background_image_url           STRING
create property User.screen_name                            STRING
create property User.url                                    STRING
create property User.listed_count                           INTEGER
create property User.description                            STRING
create property User.statuses_count                         LONG
create property User.profile_background_tile                STRING
create property User.favorite_count                         INTEGER
create property User.entities                               EMBEDDEDLIST
# AQUI IRIA EL CONTENIDO
create property User.status                                 EMBEDDEDMAP
# AQUI IRIA EL CONTENIDO
# Debajo podría ser BOOLEAN
create property User.notifications                          STRING
create property User.time_zone                              STRING
create property User.profile_image_url                      STRING
create property User.profile_text_color                     STRING
# Debajo podría ser BOOLEAN
create property User.default_profile                        STRING
create property User.created_at                             STRING
create property User.profile_banner_url                     STRING
create property User.name                                   STRING
# Debajo podría ser BOOLEAN
create property User.geo_enabled                            STRING
# Debajo podría ser BOOLEAN
create property User.default_profile_image                  STRING
#create property User.metrics                                EMBEDDEDMAP
create property User.pending                                BOOLEAN
create property User.depth                                  INTEGER

create index User.id                                        UNIQUE
create index User.pending                                   NOTUNIQUE_HASH_INDEX



# Create Tweet vertex
create class Tweet extends V

# Create User property
create property Tweet.contributors                  EMBEDDEDLIST
create property Tweet.in_reply_to_status_id	        INTEGER
create property Tweet.user_id                       LONG
create property Tweet.withheld_scope                STRING
create property Tweet.quoted_status_id              INTEGER
create property Tweet.retweet_count                 INTEGER
create property Tweet.truncated                     STRING
# Debajo podria ser BOOLEAN
create property Tweet.lang                          STRING
create property Tweet.withheld_countries            EMBEDDEDLIST
create property Tweet.quoted_status_id_str          STRING
create property Tweet.id                            LONG
create property Tweet.coordinates                   EMBEDDEDMAP
# Debajo podria ser BOOLEAN
create property Tweet.withheld_copyright            STRING
create property Tweet.in_reply_to_status_id_str     STRING
create property Tweet.id_str                        STRING
create property Tweet.source                        STRING
create property Tweet.in_reply_to_user_id           INTEGER
create property Tweet.in_reply_to_user_id_str       STRING
create property Tweet.favorite_count                INTEGER
# Debajo podría ser BOOLEAN
create property Tweet.possibly_sensitive            STRING
create property Tweet.place                         EMBEDDEDMAP
# AQUI IRIA EL CONTENIDO
create property Tweet.current_user_retweet          EMBEDDEDMAP
# AQUI IRIA EL CONTENIDO
create property Tweet.in_reply_to_screen_name       STRING
create property Tweet.scopes                        EMBEDDEDMAP
create property Tweet.entities                      EMBEDDEDMAP
create property Tweet.retweeted_status              EMBEDDEDMAP
create property Tweet.quoted_status                 EMBEDDEDMAP
create property Tweet.topics                        EMBEDDEDLIST
create property Tweet.text                          STRING
create property Tweet.filter_level                  STRING
create property Tweet.created_at                    STRING
#create property Tweet.metrics                       EMBEDDEDMAP

create index Tweet.id                               UNIQUE
# create index Tweet.topic                            NOTUNIQUE

create class Topic extends V

create property Topic.id                            LONG
create property Topic.name                          STRING
create property Topic.last_tweet                    STRING
create property Topic.tweet_count                   INTEGER
create property Topic.user_count                    INTEGER


create class User_metrics extends V

create property User_metrics.id                     LONG
create property User_metrics.lastMetrics            BOOLEAN
# Debajo podría ser STRING
create property User_metrics.date                   DATE
create property User_metrics.timestamp              DOUBLE
create property User_metrics.followers              INTEGER
create property User_metrics.following              INTEGER
create property User_metrics.statuses_count         INTEGER
create property User_metrics.influence              DOUBLE
create property User_metrics.influenceUnnormalized  DOUBLE
create property User_metrics.followRelationScore    DOUBLE
create property User_metrics.voice_t                DOUBLE
create property User_metrics.voice_r                DOUBLE
create property User_metrics.relevance              DOUBLE
create property User_metrics.tweetRatio             DOUBLE
create property User_metrics.impact                 DOUBLE
create property User_metrics.lastUpdated            STRING
# create property User_metrics.repliedRatio           DOUBLE
# create property User_metrics.hIndexFav              DOUBLE
# create property User_metrics.popularity             DOUBLE
# create property User_metrics.replyRatio             DOUBLE
# create property User_metrics.hIndexRT               DOUBLE
# create property User_metrics.follow_ratio           DOUBLE
# create property User_metrics.openinfluence          DOUBLE

# create property User_metrics.UI_score               DOUBLE
# create property User_metrics.UI_unnormalized        DOUBLE
# create property User_metrics.FR_score               DOUBLE
# create property User_metrics.voice_r                DOUBLE
# create property User_metrics.user_relevance         DOUBLE
# create property User_metrics.TR_score               DOUBLE

create property User_metrics.complete               BOOLEAN

create index User_metrics.id                        NOTUNIQUE
create index User_metrics.complete                  NOTUNIQUE


create class Tweet_metrics extends V

create property Tweet_metrics.id                    LONG
create property Tweet_metrics.lastMetrics           BOOLEAN
# Debajo podría ser STRING
create property Tweet_metrics.date                  DATE
create property Tweet_metrics.timestamp             DOUBLE
create property Tweet_metrics.influence             DOUBLE
create property Tweet_metrics.relevance             DOUBLE
create property Tweet_metrics.retweetCount          INTEGER
create property Tweet_metrics.favouriteCount        INTEGER
create property Tweet_metrics.lastUpdated           STRING

# create property Tweet_metrics.popularity            DOUBLE
# create property Tweet_metrics.TI_score              DOUBLE
# create property Tweet_metrics.tweet_relevance       DOUBLE

create property Tweet_metrics.complete              BOOLEAN

create index Tweet_metrics.id                       NOTUNIQUE
create index Tweet_metrics.complete                 NOTUNIQUE


create class EmotionSet extends V


# Create Edges classes
create class Follows extends E
create class Retweet extends E
create class Created_by extends E
create class Retweeted_by extends E
create class Reply extends E
create class Replied_by extends E
create class Belongs_to_topic extends E
create class Last_metrics extends E
create class hasEmotionSet extends E