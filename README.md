# Game-Shop
Full-stack website development project built by integrating PostgreSQL, Flask and Bootstrap

## Requirement
1. One AWS RDS PostgreSQL instance (where you host your database and upload your data)
2. Flask (back-end server)

## Running
Once you get all the installation set, inside the command window (terminal), at the same folder as where the flaskr is at, input:  
`set FLASK_APP=flaskr`  
`set FLASK_ENV=development`  
`flask run`  
You can see your website on http://127.0.0.1:5000/

## Features Implemented 
* **Game Information** - each game has it's own webpage which includes information such as producer, price, description and etc.
* **Game List** - a list at the homepage with at most 10 games shown in one page. user can click on the next page to continue to browse games. Initially it is ordered by alphabetic, and after the user has something in the wishlist or has bought some games, the content of the game list will vary according to the game type the user has an interest. 
* **Personal Account** - people can input account, password and email to register to be a member. After login, the content of navigation bar changes from "register/login" to "transaction history/wishlist/logout".
* **Wishlist** - customer can add/remove game to their wishlist on the game introduction page, user can see what games are in the wishlist right now and can navigate to these games' introduction page if they changed their mind. 
* **Checkout** - a function exists under wishlist webpage when there's at least one game inside the wishlist. Customer can choose one from several payments (credit, cash, ...) to complete the transaction. After the process is done, the transaction record will show up at the transaction history page with the time shows when the transaction was made.  
* **Transaction History** - the page that lists your transaction record chronologically. User can access to one transaction to see the detail by click on the transaction ID.
* **Transaction Record** - contain transaction detail includes prices, time, games bought
* **Top 10 Sold Games** - we list the top 10 sold games based on real-time data, once people buy games, it will actually affect the rank



