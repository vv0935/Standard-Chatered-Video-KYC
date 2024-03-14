const express = require('express')
const app = express()
const server=require('http').Server(app)
const io=require('socket.io')(server)
const { v4:uuidV4} =require('uuid')

app.set('view engine','ejs')
app.use(express.static('public'))

app.get('/', (req, res)=> {
    res.redirect(`/${uuidV4()}`)
})
app.get('/:room', (req,res)=>{
    res.render('room', {roomId: req.params.room})
})

io.on('connection', socket => {
    socket.on('join-room', (roomId, userId) => {
        socket.join(roomId);
        // Notify other users in the room about the new user connection
        socket.to(roomId).emit('user-connected', userId);

        // Handle disconnection event
        socket.on('disconnect', () => {
            // Notify other users in the room about the user disconnection
            socket.to(roomId).emit('user-disconnected', userId);
        });
    });
});


server.listen(3000)