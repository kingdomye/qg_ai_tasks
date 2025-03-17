//
//  main.cpp
//  区间DP
//
//  Created by 陈英锐 on 2024/10/15.
//

#include <iostream>
using namespace std;

int main() {
    int a[100005];
    int n = 0;
    while (cin >> a[++n]);
    
    int dp[100005];
    int dp2[100005];
    int ans = -1; int ans2 = -1;
    for (int i = 1; i < n; i++) {
        dp[i] = 1; dp2[i] = 1;
        for (int j = 1; j < i; j++) {
            if (a[j] >= a[i] && dp[j] + 1 >= dp[i]) {
                dp[i] = dp[j] + 1;
            }
            if (a[j] < a[i] && dp2[j] + 1 >= dp2[i]) {
                dp2[i] = dp2[j] + 1;
            }
            ans = max(ans, dp[i]);
            ans2 = max(ans2, dp2[i]);
        }
    }
    cout << ans << endl;
    cout << ans2 << endl;
    
    return 0;
}
