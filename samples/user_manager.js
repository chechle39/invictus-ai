// Simple JavaScript function for testing migration to Python
// This demonstrates common JavaScript patterns

function greetUser(name, age) {
    if (!name || age < 0) {
        throw new Error('Invalid input parameters');
    }
    
    const greeting = `Hello ${name}, you are ${age} years old!`;
    console.log(greeting);
    return greeting;
}

class UserManager {
    constructor() {
        this.users = [];
        this.nextId = 1;
    }
    
    addUser(name, email, age) {
        const user = {
            id: this.nextId++,
            name: name,
            email: email,
            age: age,
            createdAt: new Date().toISOString()
        };
        
        this.users.push(user);
        console.log(`✅ Added user: ${name}`);
        return user;
    }
    
    findUserById(id) {
        return this.users.find(user => user.id === id);
    }
    
    getUsersByAge(minAge) {
        return this.users.filter(user => user.age >= minAge);
    }
    
    getStats() {
        const totalUsers = this.users.length;
        const avgAge = totalUsers > 0 
            ? this.users.reduce((sum, user) => sum + user.age, 0) / totalUsers 
            : 0;
        
        return {
            total: totalUsers,
            averageAge: Math.round(avgAge * 100) / 100
        };
    }
}

// Async function example
async function fetchUserData(userId) {
    try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 100));
        
        const userData = {
            id: userId,
            name: `User ${userId}`,
            email: `user${userId}@example.com`,
            age: Math.floor(Math.random() * 50) + 18
        };
        
        console.log(`📥 Fetched data for user ${userId}`);
        return userData;
    } catch (error) {
        console.error(`❌ Error fetching user ${userId}:`, error);
        throw error;
    }
}

// Main execution
function main() {
    console.log('🚀 JavaScript Demo Starting...');
    
    // Test greeting function
    try {
        greetUser('Alice', 25);
        greetUser('Bob', 30);
    } catch (error) {
        console.error('Error in greeting:', error.message);
    }
    
    // Test user manager
    const manager = new UserManager();
    manager.addUser('Alice', 'alice@example.com', 25);
    manager.addUser('Bob', 'bob@example.com', 30);
    manager.addUser('Charlie', 'charlie@example.com', 22);
    
    console.log('📊 User Stats:', manager.getStats());
    console.log('👥 Adults (25+):', manager.getUsersByAge(25));
    
    console.log('✨ JavaScript demo completed!');
    console.log('Ready for Python conversion! 🐍');
}

// Run if this is the main module
if (require.main === module) {
    main();
}
