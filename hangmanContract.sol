pragma solidity ^0.4.1;

contract Hangman {
    uint8[] secretWord;
    uint8 secretWordLen;

    struct Category{
        uint8[] word;
    }
    
    mapping(uint => Category[]) category;
    uint8[] pos;

    function addCategory(uint8 _catId, uint8[] _word) public {
        category[_catId].push(Category(_word));
    }

    function setWordLen(uint8 _catId) public {
        uint8 rndWordInd = uint8(uint256(keccak256(block.timestamp)) % uint8(category[_catId].length));
        secretWord = category[_catId][rndWordInd].word;
        secretWordLen = uint8(secretWord.length);
    }

    function getWord() public returns (uint8[]) {
        return secretWord;
    }

    function getWordLen() public returns (uint8) {
        return secretWordLen;
    }

    function check(uint8 _letter) public returns (uint8[]) {
        
        for (uint8 i = 0; i < secretWordLen; i++) {
            if (secretWord[i] == _letter) {
                pos.push(i);
            }
        }

        return pos;
    }
}