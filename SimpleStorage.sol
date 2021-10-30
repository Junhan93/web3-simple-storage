// SPDX-License-Identifier: MIT
// change remote version settings to 0.6.0
pragma solidity ^0.6.0;

// all this will be compiled into EVM, ethereum virtual machine
contract SimpleStorage {
    // visibility: public
    uint256 favoriteNumber; // blank will be initialized to 0

    // struct are a way to define new types in solidity
    struct People {
        uint256 favoriteNumber;
        string name;
    }

    // dynamic array
    People[] public people;
    mapping(string => uint256) public nameToFavoriteNumber;

    function store(uint256 _favoriteNumber) public returns (uint256) {
        favoriteNumber = _favoriteNumber;
        return _favoriteNumber;
    }

    // view functions are read-only, which doesnt change state
    // pure functions just do some type of math
    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    // store object in either memory or storage:
    // memory means to store only in execution of function, store in storage means the value will persist even after function executes
    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_favoriteNumber, _name));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}
