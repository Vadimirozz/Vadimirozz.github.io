<?php
session_start();
require_once("twitteroauth.php"); // Путь к библиотеке twitteroauth
$twitteruser = "12hook165838"; // Замените на имя пользователя Twitter
$consumerkey = "adO8bRwuF4kSerPcDCCLcFuTx"; // Замените на ваш Consumer Key
$consumersecret = "ekzPZX6SYdhKzKqXqUfKtvL1oEnG2pKGWfjgnPJty6mcPrAH4A"; // Замените на ваш Consumer Secret
$accesstoken = "1765525056589910016-mUSzJskzSmftIlG4JNbmQM5ipaVpt4"; // Замените на ваш Access Token
$accesstokensecret = "d7b4A1ae625B7KwcqnATvKlsCQdRJaZ7JCdRV71MccLVk"; // Замените на ваш Access Token Secret

function getConnectionWithAccessToken($cons_key, $cons_secret, $oauth_token, $oauth_token_secret) {
    $connection = new TwitterOAuth($cons_key, $cons_secret, $oauth_token, $oauth_token_secret);
    return $connection;
}

$connection = getConnectionWithAccessToken($consumerkey, $consumersecret, $accesstoken, $accesstokensecret);

// Получаем список подписок пользователя
$friends = $connection->get("https://api.twitter.com/1.1/followers/list.json?screen_name=".$twitteruser);

echo json_encode($friends);
?>
