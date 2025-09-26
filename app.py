import streamlit as st
from blockchain import Blockchain

st.set_page_config(page_title="EduCoin - Classroom Crypto", layout="centered")
st.title("🎓 EduCoin - Classroom Cryptocurrency")

# Initialize blockchain in session
if "blockchain" not in st.session_state:
    st.session_state.blockchain = Blockchain()

blockchain = st.session_state.blockchain

st.sidebar.header("🛠️ Actions")

action = st.sidebar.radio("Choose an action:", [
    "👨‍🏫 Teacher: Reward Student",
    "💸 Transfer Coins",
    "💰 Check Balance",
    "📜 Transaction History",
    "🏆 Leaderboard"
])

if action == "👨‍🏫 Teacher: Reward Student":
    st.subheader("🎁 Reward a Student with EduCoins")
    student = st.text_input("Student name")
    if st.button("Mine 1 EduCoin"):
        if student.strip() != "":
            blockchain.mine_block(receiver=student.strip())
            st.success(f"1 EDU coin rewarded to {student} 🎉")
        else:
            st.warning("Please enter a student name.")

elif action == "💸 Transfer Coins":
    st.subheader("🔄 Transfer EduCoins Between Students")
    sender = st.text_input("Sender name")
    receiver = st.text_input("Receiver name")
    amount = st.number_input("Amount to transfer", min_value=1, step=1)
    if st.button("Transfer"):
        try:
            blockchain.transfer(sender.strip(), receiver.strip(), amount)
            st.success(f"{amount} EDU transferred from {sender} to {receiver}")
        except Exception as e:
            st.error(str(e))

elif action == "💰 Check Balance":
    st.subheader("🔎 Check Student Balance")
    user = st.text_input("Enter student name")
    if st.button("Check"):
        balance = blockchain.get_balance(user.strip())
        st.info(f"{user} has {balance} EDU coins")

elif action == "📜 Transaction History":
    st.subheader("📚 EduCoin Transaction History")
    history = blockchain.get_transaction_history()
    if not history:
        st.info("No transactions yet.")
    for txn in reversed(history):
        st.markdown(f"- {txn}")

elif action == "🏆 Leaderboard":
    st.subheader("🏅 Top Students by EDU Coins")
    leaderboard = blockchain.get_leaderboard()
    if not leaderboard:
        st.info("No coins distributed yet.")
    for rank, (user, coins) in enumerate(leaderboard, 1):
        st.write(f"{rank}. {user} - {coins} EDU")
