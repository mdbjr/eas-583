// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "./BridgeToken.sol";

contract Source is AccessControl {
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant WARDEN_ROLE = keccak256("BRIDGE_WARDEN_ROLE");
	mapping( address => bool) public approved;
	address[] public tokens;

	event Deposit( address indexed token, address indexed recipient, uint256 amount );
	event Withdrawal( address indexed token, address indexed recipient, uint256 amount );
	event Registration( address indexed token );
	event DebugLog(string message, uint256 value);

    constructor( address admin ) {
        _grantRole(DEFAULT_ADMIN_ROLE, admin);
        _grantRole(ADMIN_ROLE, admin);
        _grantRole(WARDEN_ROLE, admin);

				//owner = msg.sender;
				//bool tokenInTokens;

    }

	function deposit(address _token, address _recipient, uint256 _amount ) public {
		//YOUR CODE HERE
		bool tokenInTokens;
		tokenInTokens = false;

		for (uint256 i = 0; i < tokens.length; i++) {
				if (tokens[i] == _token) {
						tokenInTokens = true; 
				}
		}
		require(tokenInTokens==true, "Token not yet registered");
		ERC20 token = ERC20(_token);
		require(token.balanceOf(msg.sender)>=_amount, "Balance too low to deposit this amount");

		emit DebugLog("Message sender's token balance before:", token.balanceOf(msg.sender));
		emit DebugLog("Source's token balance before:", token.balanceOf(address(this)));
		emit DebugLog("Message recipient's token balance before:", token.balanceOf(_recipient));
		token.approve(address(this), _amount);
		token.transferFrom(msg.sender, address(this), _amount);
		//token.transfer(_recipient, _amount);
		emit DebugLog("Message sender's token balance After:", token.balanceOf(msg.sender));
		emit DebugLog("Source's token balance before:", token.balanceOf(address(this)));
		emit DebugLog("Message recipient's token balance After:", token.balanceOf(_recipient));
		emit Deposit(_token, _recipient, _amount);

	}

	function withdraw(address _token, address _recipient, uint256 _amount ) onlyRole(WARDEN_ROLE) public {
		//YOUR CODE HERE
		require(hasRole(WARDEN_ROLE, msg.sender),  "Caller is not the owner");
    require(_recipient != address(0), "Recipient cannot be the zero address");
  	require(_amount > 0, "Amount must be greater than zero");
		//require(ERC20(_token).balanceOf(msg.sender)>=_amount, "Balance too low to deposit this amount");

		ERC20 token = ERC20(_token);
    bool success = token.transfer(_recipient, _amount);
    require(success, "Token transfer failed");
		emit Withdrawal(_token, _recipient, _amount);
	}

	function registerToken(address _token) onlyRole(ADMIN_ROLE) public {
		//YOUR CODE HERE
		require(hasRole(DEFAULT_ADMIN_ROLE, msg.sender),  "Caller is not the owner");
		bool tokenInTokens;
		tokenInTokens = false;

		for (uint256 i = 0; i < tokens.length; i++) {
				if (tokens[i] == _token) {
						tokenInTokens = true; 
				}
		}

		require(tokenInTokens==false, "Token already registered");
    
		tokens.push(_token);
		approved[_token] = true;
		emit Registration(_token);
	
	}


}


