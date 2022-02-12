const chat = {
    1: {
        text: "Hey there! 👋 Welcome to DoctorOnTheGo's Chatbot! What seems to be the issue?",
        options: [
            {
                text: 'Store',
                next: 2
            },
            {
                text: 'Consultation',
                next: 11
            },
            {
                text: 'Account',
                next: 14
            },
            {
                text: 'Returns',
                next: 18
            },
            {
                text: 'Others',
                next: 24
            }
        ]
    },
    2: {
        text: 'What issue are you encountering with the store?',
        options: [
            {
                text: 'Items',
                next: 3
            },
            {
                text: 'Cart',
                next: 6
            },
            {
                text: 'Back',
                next: 1
            }
        ]
    },
    3: {
        text: 'Items',
        options: [
            {
                text: "How to find items",
                next: 4
            },
            {
                text: "Out of Stock",
                next: 5
            },
            {
                text: 'Back',
                next: 2
            }
        ]
    },
    4: {
        text: "If you know what you're looking for - try the search bar! For any additional items, do fill in the feedback form for us to consider adding to our store",
        options: [
            {
                text: "Okay!",
                next: 22
            }
        ]
    },
    5: {
        text: "We are very sorry that the item you need is out of stock. If you would like to be notified when the item comes back to stock, do fill in the feedback and we will take note of your request!",
        options: [
            {
                text: "Okay!",
                next: 22
            }
        ]
    },
    6: {
        text: 'Cart',
        options: [
            {
                text: "Add to Cart",
                next: 7
            },
            {
                text: "Check Out",
                next: 8
            },
            {
                text: "Back",
                next: 2
            }
        ]
    },
    7: {
        text: 'When you find a product you need, you can add it to cart through the “add to cart” button at the bottom of the product description, after selecting the quantity',
        options: [
            {
                text: "Okay!",
                next: 22
            }
        ]
    },
    8: {
        text: 'Check Out',
        options: [
            {
                text: "Item disappeared",
                next: 9
            },
            {
                text: "Incorrect order amount/total",
                next: 10
            }
        ]
    },
    9: {
        text: 'We are sorry that you were not able to complete your order. Until you have completed the checkout process, another customer may purchase the item even if it is in your cart. If it happens that the item is out of stock, the item will be removed from your cart',
        options: [
            {
                text: "Okay!",
                next: 22
            }
        ]
    },
    10: {
        text: 'Please double check the quantity of the item you have selected, you may have added an extra item into your cart. Rest assured that we will not charge any extra costs from the ones that are stated!',
        options: [
            {
                text: "Okay!",
                next: 22
            }
        ]
    },
    11: {
        text: 'What issue are you encountering with consultation?',
        options: [
            {
                text: 'Create',
                next: 12
            },
            {
                text: 'View/Update/Delete',
                next: 13
            },
            {
                text: 'Back',
                next: 1
            }
        ]
    },
    12: {
        text: 'To create an appointment, open the consultation tab, scroll down and click on Find An Appointment',
        options: [
            {
                text: "Okay!",
                next: 22
            }
        ]
    },
    13: {
        text: 'To view your current appointments, click on Find An Appointment and your appointment details will be shown on the page. To edit or delete, click on the respective buttons to do so',
        options: [
            {
                text: "Okay!",
                next: 22
            }
        ]
    },
    14: {
        text: 'What issue are you encountering with account?',
        options: [
            {
                text: 'Sign Up/Log In',
                next: 15
            },
            {
                text: 'Update Information',
                next: 16
            },
            {
                text: 'Rewards',
                next: 17
            },
            {
                text: 'Back',
                next: 1
            }
        ]
    },
    15: {
        text: 'To sign up or log in with us, click on the account button on the top right corner. If you do not currently have an account with us, you can sign up by filling in the form. If you do have an account, you can log in with your account information',
        options: [
            {
                text: "Okay!",
                next: 22
            }
        ]
    },
    16: {
        text: 'To update your account information, click on your account name at the top right corner, then click on account settings. There, you can edit your account, shipping and payment information as you wish',
        options: [
            {
                text: "Okay!",
                next: 22
            }
        ]
    },
    17: {
        text: 'If you sign up with us, every time you make a purchase, points will be credited to your account. These points can be used for discount in your future purchases with us!',
        options: [
            {
                text: "Okay!",
                next: 22
            }
        ]
    },
    18: {
        text: 'Return/refund policy',
        options: [
            {
                text: 'Returns/exchanges',
                next: 19
            },
            {
                text: 'Period for refund',
                next: 20
            },
            {
                text: 'Refund/replacement processing',
                next: 21
            },
            {
                text: 'Back',
                next: 1
            }
        ]
    },
    19: {
        text: 'We do not accept returns/exchanges due to the sensitive nature of medical supplies. However, we will refund/replace your item if a major fault occurs on our part. Please contact us to open a refund/replacement case!',
        options: [
            {
                text: "Okay!",
                next: 22
            }
        ]
    },
    20: {
        text: 'We accept refund/replacement requests for up to 30 after the date of purchase, afterwards you are not eligible to apply for a refund.',
        options: [
            {
                text: "Okay!",
                next: 22
            }
        ]
    },
    21: {
        text: 'For most refunds, it will take about 5-10 business days to review your case. An additional 1-3 business days is required for the refund to be credited through the payment method you have selected. If you have opted for a replacement, we will notify you through email to set a delivery date for the replacement.',
        options: [
            {
                text: "Okay!",
                next: 22
            }
        ]
    },
    22: {
        text: 'Any Other Issues?',
        options: [
            {
                text: "Yes",
                next: 1
            },
            {
                text: "No",
                next: 23
            }
        ]
    },
    23: {
        text: 'Thank you for visiting our website 😊',
    },
    24: {
        text: 'Please leave your additional queries/feedback in our feedback form above!',
    }
};


const bot = function () {

    const peekobot = document.getElementById('peekobot');
    const container = document.getElementById('peekobot-container');
    const inner = document.getElementById('peekobot-inner');
    let restartButton = null;

    const sleep = function (ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    };

    const scrollContainer = function () {
        inner.scrollTop = inner.scrollHeight;
    };

    const insertNewChatItem = function (elem) {
        //container.insertBefore(elem, peekobot);
        peekobot.appendChild(elem);
        scrollContainer();
        //debugger;
        elem.classList.add('activated');
    };

    const printResponse = async function (step) {
        const response = document.createElement('div');
        response.classList.add('chat-response');
        response.innerHTML = step.text;
        insertNewChatItem(response);

        await sleep(1500);

        if (step.options) {
            const choices = document.createElement('div');
            choices.classList.add('choices');
            step.options.forEach(function (option) {
                const button = document.createElement(option.url ? 'a' : 'button');
                button.classList.add('choice');
                button.innerHTML = option.text;
                if (option.url) {
                    button.href = option.url;
                } else {
                    button.dataset.next = option.next;
                }
                choices.appendChild(button);
            });
            insertNewChatItem(choices);
        } else if (step.next) {
            printResponse(chat[step.next]);
        }
    };

    const printChoice = function (choice) {
        const choiceElem = document.createElement('div');
        choiceElem.classList.add('chat-ask');
        choiceElem.innerHTML = choice.innerHTML;
        insertNewChatItem(choiceElem);
    };

    const disableAllChoices = function () {
        const choices = document.querySelectorAll('.choice');
        choices.forEach(function (choice) {
            choice.disabled = 'disabled';
        });
        return;
    };

    const handleChoice = async function (e) {

        if (!e.target.classList.contains('choice') || 'A' === e.target.tagName) {
            // Target isn't a button, but could be a child of a button.
            var button = e.target.closest('#peekobot-container .choice');

            if (button !== null) {
                button.click();
            }

            return;
        }

        e.preventDefault();
        const choice = e.target;

        disableAllChoices();

        printChoice(choice);
        scrollContainer();

        await sleep(1500);

        if (choice.dataset.next) {
            printResponse(chat[choice.dataset.next]);
        }
        // disable buttons here to prevent multiple choices
    };

    const handleRestart = function () {
        startConversation();
    }

    const startConversation = function () {
        printResponse(chat[1]);
    }

    const init = function () {
        container.addEventListener('click', handleChoice);

        restartButton = document.createElement('button');
        restartButton.innerText = "Restart";
        restartButton.classList.add('restart');
        restartButton.addEventListener('click', handleRestart);

        container.appendChild(restartButton);

        startConversation();
    };

    init();
}

bot();
