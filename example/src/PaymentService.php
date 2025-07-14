<?php
class PaymentService {
    private $balance;
    private $logs = [];

    public function __construct($balance = 1000) {
        $this->balance = $balance;
    }

    public function process($amount) {
        if ($amount <= 0) {
            $this->log('Invalid amount');
            return [
                'success' => false,
                'message' => 'Invalid amount',
                'balance' => $this->balance
            ];
        }
        if ($amount > $this->balance) {
            $this->log('Insufficient funds');
            return [
                'success' => false,
                'message' => 'Insufficient funds',
                'balance' => $this->balance
            ];
        }
        $this->balance -= $amount;
        $this->log("Processed payment: $amount");
        return [
            'success' => true,
            'message' => 'Payment processed',
            'balance' => $this->balance
        ];
    }

    private function log($msg) {
        $this->logs[] = date('Y-m-d H:i:s') . ' - ' . $msg;
    }

    public function getLogs() {
        return $this->logs;
    }
} 