// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract DreamCompanyContract {
  address payable public student;
  address payable public teacher;
  address public dreamCompany;
  uint public contractAmount;
  bool public isHired;

  constructor(address payable _student,address payable _teacher, address _dreamCompany, uint _contractAmount ){
    student = _student;
    teacher = _teacher;
    dreamCompany = _dreamCompany;
    contractAmount = _contractAmount;
    isHired = false; 
  }

  function hire() external{
    require(msg.sender == dreamCompany,"Only the dream company can trigger the hire function");
    isHired = true;
  }

  function payTeacher() external{
    require(isHired,"The student must be hired before making the payment");
    teacher.transfer(contractAmount);
  }
}
