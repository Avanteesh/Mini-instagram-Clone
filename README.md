# A social media application

## enables users to share Only photos (as of now!) and follow, like and comment on other users profiles

<div>
  <img height="100" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/fastapi/fastapi-original.svg" />
  <img height="100" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/sqlite/sqlite-original.svg" />
  <img height="100" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" />
  <img height="100" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/redis/redis-original.svg"/>
</div>

<p>
  For authentication The application uses JWT tokens stored in The browser cookie Which definetly isn't most secure in todays standard. Regardless here is my attempt building it.
  <b>(Further updates forthcoming)</b>
</p>

<details>
<summary>Project External Dependencies</summary>
<ul>
<li>Python framework FastAPI (version 0.0.6 CLI)</li>
<li>SQLmodel (SQL ORM) using sqlite3</li>
<li>Redis (7.0.5) with python connector</li>
<li>Redis and Redis connector with python</li>
<li>passlib (Crypto library)</li>
<li>jose for JSON Web token handling!</li>
</ul>
</details>


<h4>Make sure to create a .env file with the variables: (SECRET_KEY, TOKEN_EXPIRE_TIME, ALGORITHM)</h4>

<h5>Run the server with</h5>

```
$: fastapi dev main.py
```
