function openTab (tabName) {
  var tabs = document.getElementsByClassName('tab')
  for (var i = 0; i < tabs.length; i++) {
    tabs[i].style.display = 'none'
  }
  document.getElementById(tabName).style.display = 'block'
}

function redirectToNewDebtPage () {
  // Replace with the actual URL of your new debt page
  window.location.href = 'update_index.html'
}

document.getElementById('addSpender').addEventListener('click', function () {
  var spenderContainer = document.getElementById('spenderContainer')
  var newSpender = document.createElement('div')
  newSpender.className = 'spender'
  newSpender.innerHTML =
    '<input type="text" class="spenderName" name="spender' +
    (spenderContainer.children.length + 1) +
    '"><br>' +
    '<input type="number" class="spenderAmount" name="spenderAmount' +
    (spenderContainer.children.length + 1) +
    '"><br>'
  spenderContainer.appendChild(newSpender)
})

document.getElementById('deleteSpender').addEventListener('click', function () {
  var spenderContainer = document.getElementById('spenderContainer')
  if (spenderContainer.children.length > 0) {
    spenderContainer.removeChild(spenderContainer.lastChild)
  }
})

document
  .getElementById('paymentForm')
  .addEventListener('submit', function (event) {
    event.preventDefault()
    var amountPaid = document.getElementById('amountPaid').value
    var currencyType = document.getElementById('currencyType').value
    var spenderNames = Array.from(
      document.getElementsByClassName('spenderName')
    ).map(function (input) {
      return input.value
    })
    var spenderAmounts = Array.from(
      document.getElementsByClassName('spenderAmount')
    ).map(function (input) {
      return input.value
    })
    if (currencyType === 'rub') {
      var exchangeRate = 0.011 // Замените это на актуальный курс обмена
      var amountInUsd = amountPaid * exchangeRate
      console.log('Amount in USD: ' + amountInUsd)
    }
    var splitAmount = amountInUsd / spenderNames.length
    console.log('Each spender should pay: ' + splitAmount)
  })
