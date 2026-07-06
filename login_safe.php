<?php
header('Content-Type: application/json; charset=utf-8');

$conn = new mysqli("localhost", "root", "", "security_test");

if ($conn->connect_error) {
    echo json_encode([
        "status" => "error",
        "message" => "DB connection failed"
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    echo json_encode([
        "status" => "fail",
        "message" => "POST request required"
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

$user_id_raw = $_POST["id"] ?? "";
$user_pw_raw = $_POST["pw"] ?? "";

// 핵심 차이: 입력값 escape 처리
$user_id = mysqli_real_escape_string($conn, $user_id_raw);
$user_pw = mysqli_real_escape_string($conn, $user_pw_raw);

$sql = "SELECT username, pw FROM users WHERE id='" . $user_id . "' AND pw='" . $user_pw . "'";

$response = array();
$response["target"] = "login_safe.php";
$response["debug_sql"] = $sql;

$result = $conn->query($sql);

if ($result && $result->num_rows > 0) {
    $rows = array();

    while ($row = $result->fetch_assoc()) {
        $rows[] = $row;
    }

    $response["status"] = "success";
    $response["data"] = $rows;
} else {
    $response["status"] = "fail";
    $response["message"] = "No data found";
}

echo json_encode($response, JSON_UNESCAPED_UNICODE);

$conn->close();
?>