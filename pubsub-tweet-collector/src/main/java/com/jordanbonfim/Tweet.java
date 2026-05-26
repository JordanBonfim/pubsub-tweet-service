package com.jordanbonfim;

// author,content,country,date_time,id,language,latitude,longitude,number_of_likes,number_of_shares
public class Tweet {

    public String author;
    public String content;
    public String country;
    public String dateTime;
    public String id;
    public String language;

    public String latitude;
    public String longitude;

    public int numberOfLikes;
    public int numberOfShares;

    @Override
    public String toString() {
        return "Tweet{" +
                "author='" + author + '\'' +
                ", content='" + content + '\'' +
                ", country='" + country + '\'' +
                ", dateTime='" + dateTime + '\'' +
                ", id='" + id + '\'' +
                ", language='" + language + '\'' +
                ", latitude='" + latitude + '\'' +
                ", longitude='" + longitude + '\'' +
                ", numberOfLikes=" + numberOfLikes +
                ", numberOfShares=" + numberOfShares +
                '}';
    }

    public Tweet(String author, String content, String country, String dateTime, String id, String language, String latitude, String longitude, int numberOfLikes, int numberOfShares) {
        this.author = author;
        this.content = content;
        this.country = country;
        this.dateTime = dateTime;
        this.id = id;

        this.language = language;
        this.latitude = latitude;
        this.longitude = longitude;
        this.numberOfLikes = numberOfLikes;
        this.numberOfShares = numberOfShares;
    }
}