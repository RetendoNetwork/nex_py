Counter = {}
Counter.__index = Counter

function Counter:new(start)
    local instance = setmetatable({}, Counter)
    instance.value = start or 0
    return instance
end

function Counter:next()
    self.value = self.value + 1
    return self.value
end

return Counter