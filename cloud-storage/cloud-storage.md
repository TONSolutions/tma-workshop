
# Telegram Cloud Storage: The way to optimize UX

Basically, Telegram Cloud Storage (TCS) looks useless, because you are not able to fetch data from TCS on the server side. Because of it, the majority of developers do not use the feature. 

Of course, you can use TCS to store some non-critical data, it makes TCS more useful.

But what if you used TCS as a cache store? 

# Using Telegram Cloud Storage as a cache store

Typically, when a user starts a TMA, the application needs to authorize the user, fetch their profile data, retrieve the main data, etc. This process can take anywhere from 3 to N seconds.

There is a quite simple way to make your TMA load much faster.

## Store user's tokens

The first thing you need to do is to store refresh and access tokens in TCS.

The only thing the front-end does almost every time in the context of TMA is authorize a user.

Let's make it simplier:

```javascript
const { refreshToken, accessToken } = dataProvider;
window.Telegram.WebApp.CloudStorage.setItem("accessToken", accessToken);
window.Telegram.WebApp.CloudStorage.setItem("refreshToken", refreshToken);
```

And then you can easily fetch them:
```javascript
window.Telegram.WebApp.CloudStorage.getItem("accessToken", (err, accessToken) => {
    if (err || !accessToken) {
        // in edge cases you can fetch tokens from your backend
        return getAccessToken();
    }

    setAccessToken(accessToken);
});

window.Telegram.WebApp.CloudStorage.getItem("refreshToken", (err, refreshToken) => {
    if (err || !refreshToken) {
        // in edge cases you can fetch tokens from your backend
        return getRefreshToken();
    }

    setRefreshToken(refreshToken);
});
```

## Efficient Data Management: Storing and Invalidating Cached Information

For example, if your front-end fetches profile information, it should do so only once and then update the information if any changes occur.

```javascript
const userProfile = {
    firstName: "Chris",
    lastName: "Solutions",
    avatar: "https://some-avatar.com",
    username: "candyflipline",
};

window.Telegram.WebApp.CloudStorage.setItem("profile", JSON.stringify(userProfile));

const updateProfileUsername = async (profile, username) => {
    profile.username = username;
    const result = await sendDataToBackend();
    if (result === 200) {
        window.Telegram.WebApp.CloudStorage.setItem("profile", JSON.stringify(profile))
    }
}

updateProfileUsername(userProfile, "ton_solutions_eden");
```

