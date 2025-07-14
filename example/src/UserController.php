<?php
require_once 'User.php';

class UserController {
    private $users;
    public function __construct() {
        // Giả lập dữ liệu user
        $this->users = [
            new User(1, 'Alice'),
            new User(2, 'Bob'),
            new User(3, 'Charlie')
        ];
    }

    public function getUser($id) {
        foreach ($this->users as $user) {
            if ($user->id == $id) {
                return json_encode($user);
            }
        }
        return json_encode(["error" => "User not found"]);
    }

    public function getAllUsers() {
        return json_encode($this->users);
    }

    public function createUser($name) {
        $id = count($this->users) + 1;
        $user = new User($id, $name);
        $this->users[] = $user;
        return json_encode($user);
    }
} 