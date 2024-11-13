// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "./BridgeToken.sol";

contract Destination is AccessControl {
    bytes32 public constant WARDEN_ROLE = keccak256("BRIDGE_WARDEN_ROLE");
    bytes32 public constant CREATOR_ROLE = keccak256("CREATOR_ROLE");
	mapping( address => address) public underlying_tokens;
	mapping( address => address) public wrapped_tokens;
	address[] public tokens;

	event Creation( address indexed underlying_token, address indexed wrapped_token );
	event Wrap( address indexed underlying_token, address indexed wrapped_token, address indexed to, uint256 amount );
	event Unwrap( address indexed underlying_token, address indexed wrapped_token, address frm, address indexed to, uint256 amount );

    constructor( address admin ) {
        _grantRole(DEFAULT_ADMIN_ROLE, admin);
        _grantRole(CREATOR_ROLE, admin);
        _grantRole(WARDEN_ROLE, admin);
    }

	function wrap(address _underlying_token, address _recipient, uint256 _amount ) public onlyRole(WARDEN_ROLE) {
		//YOUR CODE HERE
		address tokenAddress = wrapped_tokens[_underlying_token];
		require(tokenAddress != address(0), "No BridgeToken found for this underlying asset");
		//Create an instance of the wrapped token
		BridgeToken wrapped_token = BridgeToken(tokenAddress);
		//call mint on the wrapped token
		wrapped_token.mint(address(_recipient), uint256(_amount));
		emit Wrap(address(_underlying_token), address(wrapped_token),address(_recipient), uint256(_amount ));
	}

	function unwrap(address _wrapped_token, address _recipient, uint256 _amount ) public {
		//YOUR CODE HERE
		address tokenAddress = underlying_tokens[_wrapped_token];
		BridgeToken underlying_token = BridgeToken(tokenAddress);
		BridgeToken wrapped_token = BridgeToken(_wrapped_token);
		require(wrapped_token.balanceOf(msg.sender) >= _amount, "BridgeToken: You must own tokens to burn");
		//require(address(_wrapped_token) == _msgSender, "Caller does not own the wrapped token");
		wrapped_token.burnFrom(msg.sender, uint256(_amount));
		emit Unwrap(address(underlying_token), address(_wrapped_token),address(msg.sender), address(_recipient), uint256(_amount ));


	}

	function createToken(address _underlying_token, string memory name, string memory symbol ) public onlyRole(CREATOR_ROLE) returns(address) {
		//YOUR CODE HERE
		BridgeToken newToken = new BridgeToken(_underlying_token, name, symbol, address(this));
		wrapped_tokens[_underlying_token] = address(newToken);
		underlying_tokens[address(newToken)] = _underlying_token;


		tokens.push(address(newToken));

		emit Creation(address(_underlying_token), address(newToken));
		return address(newToken);
	}

}


