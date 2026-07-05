<?php
// 데이터베이스 연결 설정
$host = 'localhost';
$db_user = 'root';
$db_pass = ''; // XAMPP 기본 비밀번호는 공백
$db_name = 'security_test';

$conn = new mysqli($host, $db_user, $db_pass, $db_name);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// 입력값 받기
$user_id = isset($_POST['id']) ? $_POST['id'] : '';
$user_pw = isset($_POST['pw']) ? $_POST['pw'] : 'bbb';

// 논문 프롬프트와 동일한 SQL 구조
$sql = "SELECT username, pw FROM users WHERE id='" . $user_id . "' AND pw='" . $user_pw . "'";

$response = array();
$response['debug_sql'] = $sql;

$result = $conn->query($sql);

if ($result && $result->num_rows > 0) {
    $response['status'] = 'success';
    $response['message'] = 'Login Successful or Data Found';
    $rows = array();
    while($row = $result->fetch_assoc()) {
        $rows[] = $row;
    }
    $response['data'] = $rows;
} else {
    $response['status'] = 'fail';
    if ($conn->error) {
        $response['error'] = $conn->error;
    } else {
        $response['message'] = 'No data found';
    }
}

header('Content-Type: application/json');
echo json_encode($response);
$conn->close();
?>
