(async () => {
    // 1. Find all Unfollow buttons
    const buttons = Array.from(document.querySelectorAll('input[value="Unfollow"]'));
    
    // 2. Set a very safe limit
    const batchSize = 50; 
    const targets = buttons.slice(0, batchSize);
    
    if (targets.length === 0) {
        console.log("✅ No non-followers found on this page. Scroll down or refresh!");
        return;
    }

    console.log(`🛡️ Starting Ultra-Safe Batch of ${targets.length}.`);
    console.log("This will take about 3-4 minutes. Keep this tab open.");

    for (let i = 0; i < targets.length; i++) {
        const btn = targets[i];
        
        // Highlight in green to show it's a safe action
        btn.closest('.d-table').style.backgroundColor = '#f6ffed'; 
        
        btn.click();
        
        console.log(`[${i+1}/${targets.length}] Unfollowed safely.`);
        
        // LONG DELAY: 4 to 6 seconds (Very human-like)
        const delay = Math.floor(Math.random() * 2000) + 4000;
        await new Promise(r => setTimeout(r, delay));
    }

    console.log("🏁 Batch of 40 finished!");
    alert("Batch complete. Take a 2-minute break before running the next 40!");
    window.location.reload();
})();
